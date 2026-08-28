"""Бизнес-логика портфолио.

Сервис зависит только от протокола репозитория и доменных исключений,
не от FastAPI и не от конкретной реализации хранилища.
"""

from typing import Protocol

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.models.portfolio import Category, PortfolioImage, PortfolioItem, Tag
from app.schemas.common import Page, PaginationParams
from app.schemas.portfolio import (
    NamedSlug,
    NamedSlugCreate,
    NamedSlugUpdate,
    PortfolioImageIn,
    PortfolioItemCreate,
    PortfolioItemRead,
    PortfolioItemUpdate,
)


class PortfolioRepositoryProtocol(Protocol):
    async def list_paginated(
        self,
        offset: int,
        limit: int,
        *,
        published_only: bool = True,
        category_slug: str | None = None,
        tag_slug: str | None = None,
    ) -> tuple[list[PortfolioItem], int]: ...

    async def get_by_slug(self, slug: str) -> PortfolioItem | None: ...

    async def get_with_relations(self, entity_id: int) -> PortfolioItem | None: ...

    async def slug_exists(self, slug: str, exclude_id: int | None = None) -> bool: ...

    async def add(self, entity: PortfolioItem) -> PortfolioItem: ...

    async def delete(self, entity: PortfolioItem) -> None: ...


class CategoryRepositoryProtocol(Protocol):
    async def list_all(self) -> list[Category]: ...

    async def get(self, entity_id: int) -> Category | None: ...

    async def slug_exists(self, slug: str, exclude_id: int | None = None) -> bool: ...

    async def add(self, entity: Category) -> Category: ...

    async def count_items(self, category_id: int) -> int: ...

    async def delete(self, entity: Category) -> None: ...


class TagRepositoryProtocol(Protocol):
    async def list_all(self) -> list[Tag]: ...

    async def get(self, entity_id: int) -> Tag | None: ...

    async def get_by_ids(self, ids: list[int]) -> list[Tag]: ...

    async def slug_exists(self, slug: str, exclude_id: int | None = None) -> bool: ...

    async def add(self, entity: Tag) -> Tag: ...

    async def delete(self, entity: Tag) -> None: ...


class PortfolioService:
    """Сценарии работы с портфолио."""

    def __init__(
        self,
        repository: PortfolioRepositoryProtocol,
        categories: CategoryRepositoryProtocol,
        tags: TagRepositoryProtocol,
    ) -> None:
        self._repository = repository
        self._categories = categories
        self._tags = tags

    async def list_items(
        self,
        pagination: PaginationParams,
        *,
        published_only: bool = True,
        category_slug: str | None = None,
        tag_slug: str | None = None,
    ) -> Page[PortfolioItemRead]:
        items, total = await self._repository.list_paginated(
            offset=pagination.offset,
            limit=pagination.limit,
            published_only=published_only,
            category_slug=category_slug,
            tag_slug=tag_slug,
        )
        return Page.create(
            items=[PortfolioItemRead.model_validate(item) for item in items],
            total=total,
            page=pagination.page,
            size=pagination.size,
        )

    async def get_by_slug(
        self, slug: str, *, published_only: bool = True
    ) -> PortfolioItemRead:
        item = await self._repository.get_by_slug(slug)
        if item is None or (published_only and not item.is_published):
            raise NotFoundError(f"Работа со slug '{slug}' не найдена")
        return PortfolioItemRead.model_validate(item)

    async def get_by_id(self, item_id: int) -> PortfolioItemRead:
        item = await self._repository.get_with_relations(item_id)
        if item is None:
            raise NotFoundError(f"Работа с id {item_id} не найдена")
        return PortfolioItemRead.model_validate(item)

    async def create(self, payload: PortfolioItemCreate) -> PortfolioItemRead:
        if await self._repository.slug_exists(payload.slug):
            raise ConflictError(f"Работа со slug '{payload.slug}' уже существует")
        category = await self._resolve_category(payload.category_id)
        tags = await self._resolve_tags(payload.tag_ids)
        item = PortfolioItem(
            title=payload.title,
            slug=payload.slug,
            description=payload.description,
            cover_image=payload.cover_image,
            is_published=payload.is_published,
            sort_order=payload.sort_order,
            category=category,
            tags=tags,
            images=self._build_images(payload.images),
        )
        await self._repository.add(item)
        loaded = await self._repository.get_with_relations(item.id)
        assert loaded is not None
        return PortfolioItemRead.model_validate(loaded)

    async def update(
        self, item_id: int, payload: PortfolioItemUpdate
    ) -> PortfolioItemRead:
        item = await self._repository.get_with_relations(item_id)
        if item is None:
            raise NotFoundError(f"Работа с id {item_id} не найдена")
        data = payload.model_dump(exclude_unset=True)
        if "slug" in data and await self._repository.slug_exists(
            data["slug"], exclude_id=item_id
        ):
            raise ConflictError(f"Работа со slug '{data['slug']}' уже существует")
        if "category_id" in data:
            item.category = await self._resolve_category(data.pop("category_id"))
        if "tag_ids" in data:
            item.tags = await self._resolve_tags(data.pop("tag_ids"))
        if "images" in data:
            item.images.clear()
            for image in self._build_images(data.pop("images") or []):
                item.images.append(image)
            if item.cover_image is None and item.images:
                item.cover_image = sorted(item.images, key=lambda img: img.sort_order)[
                    0
                ].url
        for field, value in data.items():
            setattr(item, field, value)
        await self._repository.add(item)
        loaded = await self._repository.get_with_relations(item.id)
        assert loaded is not None
        return PortfolioItemRead.model_validate(loaded)

    async def delete(self, item_id: int) -> None:
        item = await self._repository.get_with_relations(item_id)
        if item is None:
            raise NotFoundError(f"Работа с id {item_id} не найдена")
        await self._repository.delete(item)

    async def list_categories(self) -> list[NamedSlug]:
        return [
            NamedSlug.model_validate(item) for item in await self._categories.list_all()
        ]

    async def create_category(self, payload: NamedSlugCreate) -> NamedSlug:
        if await self._categories.slug_exists(payload.slug):
            raise ConflictError(f"Категория со slug '{payload.slug}' уже существует")
        entity = await self._categories.add(
            Category(name=payload.name, slug=payload.slug)
        )
        return NamedSlug.model_validate(entity)

    async def update_category(
        self, category_id: int, payload: NamedSlugUpdate
    ) -> NamedSlug:
        entity = await self._categories.get(category_id)
        if entity is None:
            raise NotFoundError("Категория не найдена")
        data = payload.model_dump(exclude_unset=True)
        if "slug" in data and await self._categories.slug_exists(
            data["slug"], exclude_id=category_id
        ):
            raise ConflictError(f"Категория со slug '{data['slug']}' уже существует")
        for field, value in data.items():
            setattr(entity, field, value)
        return NamedSlug.model_validate(entity)

    async def delete_category(self, category_id: int) -> None:
        entity = await self._categories.get(category_id)
        if entity is None:
            raise NotFoundError("Категория не найдена")
        if await self._categories.count_items(category_id):
            raise ConflictError("Нельзя удалить категорию, пока к ней привязаны работы")
        await self._categories.delete(entity)

    async def list_tags(self) -> list[NamedSlug]:
        return [NamedSlug.model_validate(item) for item in await self._tags.list_all()]

    async def create_tag(self, payload: NamedSlugCreate) -> NamedSlug:
        if await self._tags.slug_exists(payload.slug):
            raise ConflictError(f"Тег со slug '{payload.slug}' уже существует")
        entity = await self._tags.add(Tag(name=payload.name, slug=payload.slug))
        return NamedSlug.model_validate(entity)

    async def update_tag(self, tag_id: int, payload: NamedSlugUpdate) -> NamedSlug:
        entity = await self._tags.get(tag_id)
        if entity is None:
            raise NotFoundError("Тег не найден")
        data = payload.model_dump(exclude_unset=True)
        if "slug" in data and await self._tags.slug_exists(
            data["slug"], exclude_id=tag_id
        ):
            raise ConflictError(f"Тег со slug '{data['slug']}' уже существует")
        for field, value in data.items():
            setattr(entity, field, value)
        return NamedSlug.model_validate(entity)

    async def delete_tag(self, tag_id: int) -> None:
        entity = await self._tags.get(tag_id)
        if entity is None:
            raise NotFoundError("Тег не найден")
        await self._tags.delete(entity)

    async def _resolve_category(self, category_id: int | None) -> Category | None:
        if category_id is None:
            return None
        category = await self._categories.get(category_id)
        if category is None:
            raise ValidationError("Категория не найдена")
        return category

    async def _resolve_tags(self, tag_ids: list[int]) -> list[Tag]:
        unique_ids = list(dict.fromkeys(tag_ids))
        tags = await self._tags.get_by_ids(unique_ids)
        if len(tags) != len(unique_ids):
            raise ValidationError("Один или несколько тегов не найдены")
        return tags

    @staticmethod
    def _build_images(images: list[PortfolioImageIn]) -> list[PortfolioImage]:
        return [
            PortfolioImage(url=image.url, alt=image.alt, sort_order=image.sort_order)
            for image in images
        ]
