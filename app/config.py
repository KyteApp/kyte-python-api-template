"""Application configuration via Pydantic Settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration loaded from environment variables.

    All values can be overridden via env vars (case-insensitive) or a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Service identity ---
    service_name: str = Field(default="kyte-python-api-template", description="Service display name")
    service_version: str = Field(default="0.1.0", description="Semantic version")

    # --- Server ---
    host: str = Field(default="0.0.0.0", description="Bind host")
    port: int = Field(default=8000, description="Bind port")
    workers: int = Field(default=1, description="Uvicorn workers (use 1 for async)")
    instance_id: str = Field(default="local", description="Pod / instance identifier")
    public_url: str = Field(default="http://localhost:8000", description="Externally reachable URL")

    # --- Redis ---
    redis_url: str = Field(default="", description="Redis connection string, e.g. redis://localhost:6379/0")

    # --- Security ---
    api_bearer_token: str = Field(default="", description="Bearer token for protected endpoints")

    # --- Logging ---
    log_level: str = Field(default="INFO", description="Python log level")

    # --- Derived helpers ---
    @property
    def redis_configured(self) -> bool:
        """Return True when a Redis URL has been supplied."""
        return bool(self.redis_url)


# Singleton consumed throughout the app via `from app.config import settings`.
settings = Settings()
