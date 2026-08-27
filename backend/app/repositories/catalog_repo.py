"""Доступ к категориям и тегам."""

from sqlalchemy import func, select

from app.models.portfolio import Category, PortfolioItem, Tag
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    model = Category

    async def list_all(self) -> list[Category]:
        result = await self._session.execute(select(Category).order_by(Category.name))
        return list(result.scalars().all())

    async def get_by_slug(self, slug: str) -> Category | None:
        result = await self._session.execute(select(Category).where(Category.slug == slug))
        return result.scalar_one_or_none()

    async def slug_exists(self, slug: str, exclude_id: int | None = None) -> bool:
        stmt = select(Category.id).where(Category.slug == slug)
        if exclude_id is not None:
            stmt = stmt.where(Category.id != exclude_id)
        result = await self._session.execute(stmt.limit(1))
        return result.scalar_one_or_none() is not None

    async def count_items(self, category_id: int) -> int:
        result = await self._session.execute(
            select(func.count())
            .select_from(PortfolioItem)
            .where(PortfolioItem.category_id == category_id)
        )
        return int(result.scalar_one())

    async def delete(self, entity: Category) -> None:
        await self._session.delete(entity)
        await self._session.flush()


class TagRepository(BaseRepository[Tag]):
    model = Tag

    async def list_all(self) -> list[Tag]:
        result = await self._session.execute(select(Tag).order_by(Tag.name))
        return list(result.scalars().all())

    async def get_by_ids(self, ids: list[int]) -> list[Tag]:
        if not ids:
            return []
        result = await self._session.execute(select(Tag).where(Tag.id.in_(ids)))
        return list(result.scalars().all())

    async def slug_exists(self, slug: str, exclude_id: int | None = None) -> bool:
        stmt = select(Tag.id).where(Tag.slug == slug)
        if exclude_id is not None:
            stmt = stmt.where(Tag.id != exclude_id)
        result = await self._session.execute(stmt.limit(1))
        return result.scalar_one_or_none() is not None

    async def delete(self, entity: Tag) -> None:
        await self._session.delete(entity)
        await self._session.flush()
