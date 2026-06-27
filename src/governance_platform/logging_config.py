import logging
import sys


def configure_logging(app_env: str) -> logging.Logger:
    """Configure application logging and return the project logger."""
    log_level = logging.DEBUG if app_env == "local" else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    return logging.getLogger("governance_platform")

