"""Доступ к работам портфолио в БД."""

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.portfolio import Category, PortfolioItem, Tag
from app.repositories.base import BaseRepository
from app.utils.pagination import apply_pagination, count_rows


class PortfolioRepository(BaseRepository[PortfolioItem]):
    """Репозиторий работ портфолио."""

    model = PortfolioItem

    def _with_relations(self):
        return select(PortfolioItem).options(
            selectinload(PortfolioItem.category),
            selectinload(PortfolioItem.tags),
            selectinload(PortfolioItem.images),
        )

    async def list_paginated(
        self,
        offset: int,
        limit: int,
        *,
        published_only: bool = True,
        category_slug: str | None = None,
        tag_slug: str | None = None,
    ) -> tuple[list[PortfolioItem], int]:
        """Вернуть срез работ и общее количество.

        Витрина: опубликованные, sort_order по возрастанию,
        затем новые. Фильтры — по slug категории и тега.
        """
        stmt = self._with_relations()
        if published_only:
            stmt = stmt.where(PortfolioItem.is_published.is_(True))
        if category_slug:
            stmt = stmt.where(PortfolioItem.category.has(Category.slug == category_slug))
        if tag_slug:
            stmt = stmt.where(PortfolioItem.tags.any(Tag.slug == tag_slug))
        stmt = stmt.order_by(
            PortfolioItem.sort_order.asc(),
            PortfolioItem.created_at.desc(),
            PortfolioItem.id.desc(),
        )
        total = await count_rows(self._session, stmt)
        result = await self._session.execute(apply_pagination(stmt, offset, limit))
        return list(result.scalars().unique().all()), total

    async def get_by_slug(self, slug: str) -> PortfolioItem | None:
        stmt = self._with_relations().where(PortfolioItem.slug == slug)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_with_relations(self, entity_id: int) -> PortfolioItem | None:
        stmt = self._with_relations().where(PortfolioItem.id == entity_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def slug_exists(self, slug: str, exclude_id: int | None = None) -> bool:
        stmt = select(PortfolioItem.id).where(PortfolioItem.slug == slug)
        if exclude_id is not None:
            stmt = stmt.where(PortfolioItem.id != exclude_id)
        result = await self._session.execute(stmt.limit(1))
        return result.scalar_one_or_none() is not None

    async def delete(self, entity: PortfolioItem) -> None:
        await self._session.delete(entity)
        await self._session.flush()
