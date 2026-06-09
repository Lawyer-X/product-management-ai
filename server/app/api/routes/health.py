from fastapi import APIRouter
from sqlalchemy import text

from app.config import Settings, get_settings
from app.db.session import SessionDep
from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings: Settings = get_settings()
    return HealthResponse(
        status="ok",
        app=settings.app_name,
        environment=settings.environment,
    )


@router.get("/health/db", response_model=ReadinessResponse)
async def health_db(session: SessionDep) -> ReadinessResponse:
    """Verify the database connection by issuing a trivial query."""
    await session.execute(text("SELECT 1"))
    return ReadinessResponse(status="ok", database="connected")
