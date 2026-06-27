from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    project_name: str
    app_env: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    minio_endpoint: str
    qdrant_host: str
    qdrant_port: int
    ollama_host: str
    llm_model: str


def _get_env(name: str, default: str) -> str:
    return os.getenv(name, default)


def _get_int_env(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    try:
        return int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc


def load_settings() -> Settings:
    """Load local settings from environment variables with safe defaults."""
    return Settings(
        project_name=_get_env(
            "PROJECT_NAME",
            "enterprise-ai-data-governance-platform",
        ),
        app_env=_get_env("APP_ENV", "local"),
        postgres_host=_get_env("POSTGRES_HOST", "localhost"),
        postgres_port=_get_int_env("POSTGRES_PORT", 5432),
        postgres_db=_get_env("POSTGRES_DB", "governance_catalog"),
        minio_endpoint=_get_env("MINIO_ENDPOINT", "localhost:9000"),
        qdrant_host=_get_env("QDRANT_HOST", "localhost"),
        qdrant_port=_get_int_env("QDRANT_PORT", 6333),
        ollama_host=_get_env("OLLAMA_HOST", "http://localhost:11434"),
        llm_model=_get_env("LLM_MODEL", "qwen2.5"),
    )

