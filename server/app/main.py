from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.config import get_settings
from app.db.session import get_engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup logic goes here (db connections, model loading, etc.).
    settings = get_settings()
    yield
    # Dispose the connection pool on shutdown if it was ever created.
    if settings.database_url:
        await get_engine().dispose()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app


app = create_app()
