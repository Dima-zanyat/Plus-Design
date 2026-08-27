"""Общие зависимости приложения."""

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.db.session import get_session
from app.schemas.common import PaginationParams


async def get_db() -> AsyncIterator[AsyncSession]:
    """Сессия БД на время запроса."""
    async for session in get_session():
        yield session


DbSession = Annotated[AsyncSession, Depends(get_db)]
AppSettings = Annotated[Settings, Depends(get_settings)]


def get_pagination(
    page: Annotated[int, Query(ge=1, description="Номер страницы, с 1.")] = 1,
    size: Annotated[
        int, Query(ge=1, le=100, description="Количество элементов на странице.")
    ] = 12,
) -> PaginationParams:
    """Разобрать query-параметры пагинации."""
    return PaginationParams(page=page, size=size)


Pagination = Annotated[PaginationParams, Depends(get_pagination)]
