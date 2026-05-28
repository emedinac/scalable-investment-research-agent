from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Scalable Investment Research Agent"
    environment: str = "local"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"  # noqa: S104
    api_port: int = 8000

    database_url: str = "sqlite+aiosqlite:///./research.db"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    semantic_cache_ttl_seconds: int = 21_600
    semantic_cache_threshold: float = Field(default=0.92, ge=0.0, le=1.0)
    price_cache_ttl_seconds: int = 3_600

    tavily_api_key: str | None = None
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    alpha_vantage_api_key: str | None = None
    langfuse_public_key: str | None = None
    langfuse_secret_key: str | None = None
    langfuse_host: str = "http://localhost:3000"
    mlflow_tracking_uri: str = "http://localhost:5000"

    @property
    def live_search_enabled(self) -> bool:
        return bool(self.tavily_api_key)

    @property
    def live_llm_enabled(self) -> bool:
        return bool(self.openai_api_key or self.anthropic_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
