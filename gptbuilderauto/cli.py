"""
Command Line Interface for GPTbuilderauto
"""

import click
import logging
from pathlib import Path
from gptbuilderauto.core.code_generator import CodeGenerator
from gptbuilderauto.executor.code_executor import CodeExecutor
from gptbuilderauto.deployer.deployer import Deployer
from gptbuilderauto.monitor.maintenance import MaintenanceMonitor
from gptbuilderauto.utils.config import load_config
from gptbuilderauto.utils.logging import setup_logging


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def main(verbose):
    """GPTbuilderauto - Autonomous code creation, execution, deployment, and maintenance"""
    config = load_config()
    log_level = "DEBUG" if verbose else config.get("log_level", "INFO")
    setup_logging(log_level, config.get("log_file"))


@main.command()
@click.argument("requirement")
@click.option("--language", "-l", default="python", help="Programming language")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def generate(requirement, language, output):
    """Generate code based on requirements"""
    logger = logging.getLogger(__name__)

    try:
        config = load_config()
        generator = CodeGenerator(
            api_key=config.get("openai_api_key"), model=config.get("openai_model", "gpt-4")
        )

        click.echo(f"Generating {language} code for: {requirement}")
        result = generator.generate_code(requirement, language)

        if output:
            Path(output).write_text(result["code"])
            click.echo(f"Code saved to {output}")
        else:
            click.echo("\n--- Generated Code ---")
            click.echo(result["code"])
            click.echo(f"\n--- Tokens used: {result.get('tokens_used', 'N/A')} ---")

    except Exception as e:
        logger.error(f"Code generation failed: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@main.command()
@click.argument("code_file", type=click.Path(exists=True))
@click.option("--language", "-l", default="python", help="Programming language")
@click.option("--docker/--no-docker", default=True, help="Use Docker for execution")
def execute(code_file, language, docker):
    """Execute code from a file"""
    logger = logging.getLogger(__name__)

    try:
        config = load_config()
        executor = CodeExecutor(
            timeout=config.get("execution_timeout", 300),
            use_docker=docker and config.get("enable_docker", True),
            enable_sandboxing=config.get("enable_sandboxing", True),
        )

        code = Path(code_file).read_text()

        click.echo(f"Executing {language} code from {code_file}...")
        result = executor.execute_python(code)

        click.echo("\n--- Execution Output ---")
        if result["stdout"]:
            click.echo(result["stdout"])
        if result["stderr"]:
            click.echo(f"Errors:\n{result['stderr']}", err=True)
        click.echo(f"\nReturn code: {result['return_code']}")
        click.echo(f"Success: {result['success']}")

    except Exception as e:
        logger.error(f"Code execution failed: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@main.command()
@click.argument("code_file", type=click.Path(exists=True))
@click.argument("name")
@click.option("--language", "-l", default="python", help="Programming language")
@click.option("--provider", "-p", default="local", help="Deployment provider")
def deploy(code_file, name, language, provider):
    """Deploy code to target environment"""
    logger = logging.getLogger(__name__)

    try:
        config = load_config()
        deployer = Deployer(deploy_path=config.get("deploy_path"), provider=provider)

        code = Path(code_file).read_text()

        click.echo(f"Deploying {name} to {provider}...")
        result = deployer.deploy_code(code, name, language)

        if result["success"]:
            click.echo("\nDeployment successful!")
            click.echo(f"Deployment name: {result['deployment_name']}")
            click.echo(f"Location: {result['deployment_path']}")
        else:
            click.echo(f"\nDeployment failed: {result.get('error')}", err=True)

    except Exception as e:
        logger.error(f"Deployment failed: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@main.command()
def list_deployments():
    """List all deployments"""
    logger = logging.getLogger(__name__)

    try:
        config = load_config()
        deployer = Deployer(deploy_path=config.get("deploy_path"))

        deployments = deployer.list_deployments()

        if not deployments:
            click.echo("No deployments found.")
            return

        click.echo(f"\nFound {len(deployments)} deployment(s):\n")
        for dep in deployments:
            click.echo(f"  - {dep['name']}")
            click.echo(f"    Path: {dep['path']}")
            click.echo(f"    Created: {dep['created']}")
            click.echo()

    except Exception as e:
        logger.error(f"Failed to list deployments: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@main.command()
@click.argument("deployment_path", type=click.Path(exists=True))
def monitor(deployment_path):
    """Monitor a deployment"""
    logger = logging.getLogger(__name__)

    try:
        monitor = MaintenanceMonitor()

        click.echo(f"Performing health check on {deployment_path}...")
        result = monitor.health_check(deployment_path)

        click.echo("\n--- Health Check Results ---")
        click.echo(f"Status: {result['status']}")
        if result.get("main_file"):
            click.echo(f"Main file: {result['main_file']}")
            click.echo(f"File size: {result['file_size']} bytes")
            click.echo(f"Syntax valid: {result.get('syntax_valid', 'N/A')}")
        if result.get("message"):
            click.echo(f"Message: {result['message']}")
        click.echo(f"Timestamp: {result['timestamp']}")

    except Exception as e:
        logger.error(f"Monitoring failed: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@main.command()
@click.argument("requirement")
@click.option("--language", "-l", default="python", help="Programming language")
@click.option("--name", "-n", required=True, help="Deployment name")
@click.option("--execute/--no-execute", default=True, help="Execute before deploying")
def auto(requirement, language, name, execute):
    """Fully autonomous: generate, execute, and deploy code"""
    logger = logging.getLogger(__name__)

    try:
        config = load_config()

        # Generate
        click.echo("=== Step 1: Code Generation ===")
        generator = CodeGenerator(
            api_key=config.get("openai_api_key"), model=config.get("openai_model", "gpt-4")
        )

        click.echo(f"Generating {language} code for: {requirement}")
        gen_result = generator.generate_code(requirement, language)
        code = gen_result["code"]
        click.echo(f"✓ Generated {gen_result.get('tokens_used', 'N/A')} tokens")

        # Execute (if enabled)
        if execute:
            click.echo("\n=== Step 2: Code Execution ===")
            executor = CodeExecutor(
                timeout=config.get("execution_timeout", 300),
                use_docker=config.get("enable_docker", True),
                enable_sandboxing=config.get("enable_sandboxing", True),
            )

            click.echo("Testing generated code...")
            exec_result = executor.execute_python(code)

            if exec_result["success"]:
                click.echo("✓ Code executed successfully")
                if exec_result["stdout"]:
                    click.echo(f"Output: {exec_result['stdout'][:200]}")
            else:
                click.echo(f"✗ Execution failed: {exec_result['stderr']}", err=True)
                click.echo("Continuing with deployment anyway...")

        # Deploy
        click.echo("\n=== Step 3: Deployment ===")
        deployer = Deployer(
            deploy_path=config.get("deploy_path"), provider=config.get("deploy_provider", "local")
        )

        click.echo(f"Deploying {name}...")
        deploy_result = deployer.deploy_code(
            code,
            name,
            language,
            metadata={
                "requirement": requirement,
                "tokens_used": gen_result.get("tokens_used"),
                "auto_generated": True,
            },
        )

        if deploy_result["success"]:
            click.echo(f"✓ Deployed to {deploy_result['deployment_path']}")
        else:
            click.echo(f"✗ Deployment failed: {deploy_result.get('error')}", err=True)

        # Monitor
        click.echo("\n=== Step 4: Health Check ===")
        monitor = MaintenanceMonitor()
        health = monitor.health_check(deploy_result["deployment_path"])
        click.echo(f"Status: {health['status']}")

        click.echo("\n=== Autonomous Process Complete ===")
        click.echo(f"Deployment location: {deploy_result['deployment_path']}")

    except Exception as e:
        logger.error(f"Autonomous process failed: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
