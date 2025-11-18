"""
Code Executor Module - Safely executes generated code
"""

import os
import subprocess
import tempfile
import logging
from typing import Dict, Optional, List
from pathlib import Path
import docker


class CodeExecutor:
    """
    Executes code in a sandboxed environment
    """

    def __init__(self, timeout: int = 300, use_docker: bool = True, enable_sandboxing: bool = True):
        """
        Initialize the code executor

        Args:
            timeout: Maximum execution time in seconds
            use_docker: Use Docker for isolation
            enable_sandboxing: Enable additional sandboxing measures
        """
        self.timeout = timeout
        self.use_docker = use_docker
        self.enable_sandboxing = enable_sandboxing
        self.logger = logging.getLogger(__name__)

        if use_docker:
            try:
                self.docker_client = docker.from_env()
            except Exception as e:
                self.logger.warning(f"Docker not available: {e}")
                self.use_docker = False
                self.docker_client = None
        else:
            self.docker_client = None

    def execute_python(
        self, code: str, args: Optional[List[str]] = None, env_vars: Optional[Dict[str, str]] = None
    ) -> Dict[str, any]:
        """
        Execute Python code

        Args:
            code: Python code to execute
            args: Command line arguments
            env_vars: Environment variables

        Returns:
            Execution result with stdout, stderr, return code
        """
        if self.use_docker:
            return self._execute_in_docker(code, "python", args, env_vars)
        else:
            return self._execute_locally(code, "python", args, env_vars)

    def _execute_locally(
        self,
        code: str,
        language: str,
        args: Optional[List[str]] = None,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> Dict[str, any]:
        """
        Execute code locally in a temporary file

        Args:
            code: Code to execute
            language: Programming language
            args: Command line arguments
            env_vars: Environment variables

        Returns:
            Execution result
        """
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=f".{self._get_extension(language)}", delete=False
        ) as f:
            f.write(code)
            temp_file = f.name

        try:
            cmd = self._get_command(language, temp_file, args)

            env = os.environ.copy()
            if env_vars:
                env.update(env_vars)

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=self.timeout, env=env
            )

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            self.logger.error(f"Execution timeout after {self.timeout} seconds")
            return {
                "stdout": "",
                "stderr": f"Execution timeout after {self.timeout} seconds",
                "return_code": -1,
                "success": False,
            }
        except Exception as e:
            self.logger.error(f"Execution failed: {str(e)}")
            return {"stdout": "", "stderr": str(e), "return_code": -1, "success": False}
        finally:
            try:
                os.unlink(temp_file)
            except OSError:
                pass

    def _execute_in_docker(
        self,
        code: str,
        language: str,
        args: Optional[List[str]] = None,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> Dict[str, any]:
        """
        Execute code in a Docker container

        Args:
            code: Code to execute
            language: Programming language
            args: Command line arguments
            env_vars: Environment variables

        Returns:
            Execution result
        """
        if not self.docker_client:
            return self._execute_locally(code, language, args, env_vars)

        image = self._get_docker_image(language)

        try:
            # Create temporary directory for code
            with tempfile.TemporaryDirectory() as tmpdir:
                code_file = Path(tmpdir) / f"code.{self._get_extension(language)}"
                code_file.write_text(code)

                # Run in container
                container = self.docker_client.containers.run(
                    image,
                    command=self._get_container_command(
                        language, "code." + self._get_extension(language), args
                    ),
                    volumes={tmpdir: {"bind": "/workspace", "mode": "ro"}},
                    working_dir="/workspace",
                    environment=env_vars or {},
                    remove=True,
                    detach=False,
                    stdout=True,
                    stderr=True,
                    mem_limit="512m",
                    network_disabled=True if self.enable_sandboxing else False,
                )

                return {
                    "stdout": (
                        container.decode("utf-8")
                        if isinstance(container, bytes)
                        else str(container)
                    ),
                    "stderr": "",
                    "return_code": 0,
                    "success": True,
                }
        except docker.errors.ContainerError as e:
            self.logger.error(f"Container execution failed: {str(e)}")
            return {
                "stdout": e.stdout.decode("utf-8") if e.stdout else "",
                "stderr": e.stderr.decode("utf-8") if e.stderr else str(e),
                "return_code": e.exit_status,
                "success": False,
            }
        except Exception as e:
            self.logger.error(f"Docker execution failed: {str(e)}")
            return {"stdout": "", "stderr": str(e), "return_code": -1, "success": False}

    def _get_extension(self, language: str) -> str:
        """Get file extension for language"""
        extensions = {
            "python": "py",
            "javascript": "js",
            "java": "java",
            "go": "go",
            "rust": "rs",
        }
        return extensions.get(language.lower(), "txt")

    def _get_command(
        self, language: str, file_path: str, args: Optional[List[str]] = None
    ) -> List[str]:
        """Get execution command for language"""
        args = args or []
        commands = {
            "python": ["python3", file_path] + args,
            "javascript": ["node", file_path] + args,
        }
        return commands.get(language.lower(), ["cat", file_path])

    def _get_docker_image(self, language: str) -> str:
        """Get Docker image for language"""
        images = {
            "python": "python:3.11-slim",
            "javascript": "node:18-slim",
        }
        return images.get(language.lower(), "python:3.11-slim")

    def _get_container_command(
        self, language: str, filename: str, args: Optional[List[str]] = None
    ) -> List[str]:
        """Get container execution command"""
        args = args or []
        commands = {
            "python": ["python3", filename] + args,
            "javascript": ["node", filename] + args,
        }
        return commands.get(language.lower(), ["cat", filename])
