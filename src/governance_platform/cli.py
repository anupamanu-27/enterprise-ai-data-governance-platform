from governance_platform.config import load_settings
from governance_platform.logging_config import configure_logging


def main() -> None:
    """Run a small health check for the local project setup."""
    settings = load_settings()
    logger = configure_logging(settings.app_env)
    logger.info("Governance platform CLI is ready")
    print(f"{settings.project_name} is ready in {settings.app_env} mode")

