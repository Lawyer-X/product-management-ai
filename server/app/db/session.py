from collections.abc import AsyncGenerator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import URL, make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings


def _async_url(raw: str) -> URL:
    """Normalize a connection string to the async psycopg driver.

    Supabase hands out plain `postgresql://...` strings, which SQLAlchemy maps
    to the (sync, uninstalled) psycopg2 dialect. Force the `postgresql+psycopg`
    driver so a copy-pasted Supabase URL works without manual editing.
    """
    url = make_url(raw)
    if url.drivername in ("postgresql", "postgres", "postgresql+psycopg2"):
        url = url.set(drivername="postgresql+psycopg")
    return url


@lru_cache
def get_engine() -> AsyncEngine:
    settings = get_settings()
    if not settings.database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy .env.example to .env and add your "
            "Supabase connection string."
        )

    # Supabase's transaction pooler (pgbouncer) doesn't support prepared
    # statements, so disable psycopg's prepared-statement cache there.
    connect_args: dict = {}
    if settings.db_use_pooler:
        connect_args["prepare_threshold"] = None

    return create_async_engine(
        _async_url(settings.database_url),
        echo=settings.debug,
        pool_pre_ping=True,
        connect_args=connect_args,
    )


@lru_cache
def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=get_engine(),
        expire_on_commit=False,
        autoflush=False,
    )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a database session."""
    async with get_sessionmaker()() as session:
        yield session


# Annotated dependency for route signatures: `session: SessionDep`.
SessionDep = Annotated[AsyncSession, Depends(get_session)]
