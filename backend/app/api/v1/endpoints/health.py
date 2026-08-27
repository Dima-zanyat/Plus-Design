"""Healthcheck."""

from fastapi import APIRouter, status
from sqlalchemy import text

from app.dependencies import DbSession

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK, summary="Проверка живости")
async def health() -> dict[str, str]:
    """Ответить, что приложение поднято."""
    return {"status": "ok"}


@router.get("/health/db", status_code=status.HTTP_200_OK, summary="Проверка БД")
async def health_db(session: DbSession) -> dict[str, str]:
    """Проверить, что соединение с БД живое."""
    await session.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}
