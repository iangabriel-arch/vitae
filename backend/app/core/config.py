"""
Central app configuration, loaded from environment variables (.env).
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "Vitae API"
    ENV: str = "development"  # development | staging | production

    # --- Database ---
    DATABASE_URL: str = "postgresql://vitae:vitae_dev@localhost:5432/vitae_db"

    # --- Auth / JWT ---
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h

    # --- CORS ---
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — avoids re-parsing .env on every import."""
    return Settings()


settings = get_settings()
