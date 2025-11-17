"""
Deployer Module - Handles automated deployment
"""

import os
import shutil
import logging
from typing import Dict, Optional, List
from pathlib import Path
from datetime import datetime
import git


class Deployer:
    """
    Handles automated deployment of generated code
    """

    def __init__(self, deploy_path: Optional[str] = None, provider: str = "local"):
        """
        Initialize the deployer

        Args:
            deploy_path: Path for deployments
            provider: Deployment provider (local, git, docker)
        """
        self.deploy_path = Path(
            deploy_path or os.getenv("DEPLOY_PATH", "/tmp/gptbuilder_deployments")
        )
        self.provider = provider
        self.logger = logging.getLogger(__name__)

        # Create deployment directory
        self.deploy_path.mkdir(parents=True, exist_ok=True)

    def deploy_code(
        self, code: str, name: str, language: str = "python", metadata: Optional[Dict] = None
    ) -> Dict[str, str]:
        """
        Deploy generated code

        Args:
            code: Code to deploy
            name: Deployment name
            language: Programming language
            metadata: Additional metadata

        Returns:
            Deployment information
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        deployment_name = f"{name}_{timestamp}"
        deployment_dir = self.deploy_path / deployment_name

        try:
            # Create deployment directory
            deployment_dir.mkdir(parents=True, exist_ok=True)

            # Write code file
            extension = self._get_extension(language)
            code_file = deployment_dir / f"main.{extension}"
            code_file.write_text(code)

            # Write metadata
            if metadata:
                import json

                metadata_file = deployment_dir / "metadata.json"
                metadata_file.write_text(json.dumps(metadata, indent=2))

            # Create README
            readme = self._generate_readme(name, language, metadata)
            (deployment_dir / "README.md").write_text(readme)

            self.logger.info(f"Code deployed to {deployment_dir}")

            return {
                "deployment_name": deployment_name,
                "deployment_path": str(deployment_dir),
                "code_file": str(code_file),
                "success": True,
            }
        except Exception as e:
            self.logger.error(f"Deployment failed: {str(e)}")
            return {"deployment_name": deployment_name, "error": str(e), "success": False}

    def deploy_to_git(
        self, code: str, name: str, repo_path: str, branch: str = "main", language: str = "python"
    ) -> Dict[str, str]:
        """
        Deploy code to a git repository

        Args:
            code: Code to deploy
            name: Deployment name
            repo_path: Path to git repository
            branch: Branch to commit to
            language: Programming language

        Returns:
            Deployment information
        """
        try:
            repo = git.Repo(repo_path)

            # Create file in repo
            extension = self._get_extension(language)
            file_path = Path(repo_path) / f"{name}.{extension}"
            file_path.write_text(code)

            # Commit changes
            repo.index.add([str(file_path)])
            repo.index.commit(f"Deploy {name} via GPTbuilderauto")

            # Push if remote exists
            if repo.remotes:
                origin = repo.remote("origin")
                origin.push(branch)

            self.logger.info(f"Code deployed to git repository at {repo_path}")

            return {
                "deployment_name": name,
                "repo_path": repo_path,
                "file_path": str(file_path),
                "branch": branch,
                "success": True,
            }
        except Exception as e:
            self.logger.error(f"Git deployment failed: {str(e)}")
            return {"deployment_name": name, "error": str(e), "success": False}

    def list_deployments(self) -> List[Dict[str, str]]:
        """
        List all deployments

        Returns:
            List of deployment information
        """
        deployments = []

        try:
            for item in self.deploy_path.iterdir():
                if item.is_dir():
                    metadata_file = item / "metadata.json"
                    metadata = {}

                    if metadata_file.exists():
                        import json

                        metadata = json.loads(metadata_file.read_text())

                    deployments.append(
                        {
                            "name": item.name,
                            "path": str(item),
                            "created": datetime.fromtimestamp(item.stat().st_ctime).isoformat(),
                            "metadata": metadata,
                        }
                    )
        except Exception as e:
            self.logger.error(f"Failed to list deployments: {str(e)}")

        return deployments

    def delete_deployment(self, deployment_name: str) -> bool:
        """
        Delete a deployment

        Args:
            deployment_name: Name of deployment to delete

        Returns:
            Success status
        """
        deployment_dir = self.deploy_path / deployment_name

        try:
            if deployment_dir.exists():
                shutil.rmtree(deployment_dir)
                self.logger.info(f"Deleted deployment {deployment_name}")
                return True
            else:
                self.logger.warning(f"Deployment {deployment_name} not found")
                return False
        except Exception as e:
            self.logger.error(f"Failed to delete deployment: {str(e)}")
            return False

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

    def _generate_readme(self, name: str, language: str, metadata: Optional[Dict] = None) -> str:
        """Generate README for deployment"""
        readme = f"""# {name}

Automatically generated and deployed by GPTbuilderauto

## Language
{language}

## Deployment Information
- Deployed: {datetime.now().isoformat()}
"""

        if metadata:
            readme += "\n## Metadata\n"
            for key, value in metadata.items():
                readme += f"- **{key}**: {value}\n"

        readme += """
## Usage
Run the main file to execute the code.

---
*Generated by GPTbuilderauto - Autonomous code creation, execution, deployment, and maintenance*
"""
        return readme
