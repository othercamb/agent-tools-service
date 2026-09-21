from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All configuration comes from environment variables or a local .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "agent-tools-service"
    log_level: str = "INFO"
    database_path: str = "data/app.db"
    webhook_secret: str = "change-me"
    litellm_base_url: str = "http://localhost:4000"
    litellm_api_key: str = ""
    http_timeout_seconds: float = 10.0


@lru_cache
def get_settings() -> Settings:
    return Settings()
