"""
Configuration utilities
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv


def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables

    Returns:
        Configuration dictionary
    """
    load_dotenv()

    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-4"),
        "execution_timeout": int(os.getenv("EXECUTION_TIMEOUT", "300")),
        "enable_docker": os.getenv("ENABLE_DOCKER", "true").lower() == "true",
        "deploy_provider": os.getenv("DEPLOY_PROVIDER", "local"),
        "deploy_path": os.getenv("DEPLOY_PATH", "/tmp/gptbuilder_deployments"),
        "enable_sandboxing": os.getenv("ENABLE_SANDBOXING", "true").lower() == "true",
        "max_execution_time": int(os.getenv("MAX_EXECUTION_TIME", "600")),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "log_file": os.getenv("LOG_FILE", "gptbuilder.log"),
    }


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration

    Args:
        config: Configuration dictionary

    Returns:
        True if configuration is valid
    """
    required_keys = ["openai_api_key"]

    for key in required_keys:
        if not config.get(key):
            return False

    return True
