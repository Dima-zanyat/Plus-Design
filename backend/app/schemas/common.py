"""Общие схемы: пагинация и ошибки."""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Параметры постраничной выборки (offset/limit)."""

    page: int = Field(default=1, ge=1, description="Номер страницы, начиная с 1.")
    size: int = Field(default=12, ge=1, le=100, description="Размер страницы.")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size


class Page(BaseModel, Generic[T]):
    """Страница результатов с метаданными для навигации."""

    items: list[T]
    total: int = Field(description="Общее количество записей, удовлетворяющих фильтру.")
    page: int
    size: int
    pages: int = Field(description="Общее количество страниц.")
    has_next: bool
    has_prev: bool

    @classmethod
    def create(cls, items: list[T], total: int, page: int, size: int) -> "Page[T]":
        pages = (total + size - 1) // size if size else 0
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1 and total > 0,
        )


class ErrorResponse(BaseModel):
    """Единый формат тела ошибки."""

    detail: str
