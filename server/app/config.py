from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "product-management-ai"
    environment: str = "development"
    debug: bool = True

    # Comma-separated list of allowed CORS origins.
    cors_origins: list[str] = ["http://localhost:3000"]

    # Supabase Postgres connection string. Use the SQLAlchemy async driver,
    # e.g. postgresql+psycopg://postgres:<pwd>@<host>:5432/postgres
    database_url: str = ""

    # Set True when connecting through Supabase's transaction pooler (port 6543);
    # pgbouncer in transaction mode does not support prepared statements.
    db_use_pooler: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
