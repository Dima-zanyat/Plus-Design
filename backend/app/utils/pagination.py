"""Утилиты постраничной выборки для слоя репозиториев."""

from typing import TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


def apply_pagination(stmt: Select[tuple[T]], offset: int, limit: int) -> Select[tuple[T]]:
    """Наложить offset/limit на готовый запрос."""
    return stmt.offset(offset).limit(limit)


async def count_rows(session: AsyncSession, stmt: Select[tuple[T]]) -> int:
    """Посчитать количество строк запроса без сортировки и срезов."""
    count_stmt = select(func.count()).select_from(
        stmt.order_by(None).subquery()
    )
    result = await session.execute(count_stmt)
    return int(result.scalar_one())
