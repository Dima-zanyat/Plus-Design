"""Доступ к заявкам в БД."""

from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select

from app.models.lead import Lead
from app.repositories.base import BaseRepository
from app.utils.pagination import apply_pagination, count_rows


class LeadRepository(BaseRepository[Lead]):
    """Репозиторий заявок на проект."""

    model = Lead

    async def count_recent_by_phone(self, phone: str, within: timedelta) -> int:
        """Сколько заявок с этого телефона пришло за последний интервал.

        Используется как простая защита от повторной отправки формы.
        """
        since = datetime.now(UTC) - within
        stmt = (
            select(func.count())
            .select_from(Lead)
            .where(Lead.phone == phone, Lead.created_at >= since)
        )
        result = await self._session.execute(stmt)
        return int(result.scalar_one())

    async def list_paginated(self, offset: int, limit: int) -> tuple[list[Lead], int]:
        stmt = select(Lead).order_by(Lead.created_at.desc(), Lead.id.desc())
        total = await count_rows(self._session, stmt)
        result = await self._session.execute(apply_pagination(stmt, offset, limit))
        return list(result.scalars().all()), total
