"""Pydantic-схемы портфолио, категорий, тегов и галереи."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class NamedSlug(BaseModel):
    """Категория или тег в ответах."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str


class NamedSlugCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    slug: str = Field(
        min_length=1,
        max_length=140,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )


class NamedSlugUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=140,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )


class PortfolioImageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    alt: str
    sort_order: int


class PortfolioImageIn(BaseModel):
    url: str = Field(min_length=1, max_length=500)
    alt: str = Field(default="", max_length=200)
    sort_order: int = 0


class PortfolioItemBase(BaseModel):
    """Общие поля работы портфолио."""

    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(
        min_length=1,
        max_length=220,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        description="Человекочитаемый идентификатор в URL, kebab-case.",
    )
    description: str = Field(default="", max_length=10_000)
    cover_image: str | None = Field(default=None, max_length=500)
    is_published: bool = True
    sort_order: int = 0


class PortfolioItemWrite(PortfolioItemBase):
    category_id: int | None = None
    tag_ids: list[int] = Field(default_factory=list)
    images: list[PortfolioImageIn] = Field(default_factory=list)

    @model_validator(mode="after")
    def _cover_from_gallery(self) -> "PortfolioItemWrite":
        if not self.cover_image and self.images:
            first = sorted(self.images, key=lambda img: img.sort_order)[0]
            self.cover_image = first.url
        return self


class PortfolioItemCreate(PortfolioItemWrite):
    """Тело запроса на создание работы."""


class PortfolioItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=220,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )
    description: str | None = Field(default=None, max_length=10_000)
    cover_image: str | None = Field(default=None, max_length=500)
    is_published: bool | None = None
    sort_order: int | None = None
    category_id: int | None = None
    tag_ids: list[int] | None = None
    images: list[PortfolioImageIn] | None = None


class PortfolioItemRead(PortfolioItemBase):
    """Представление работы в ответах API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    category: NamedSlug | None = None
    tags: list[NamedSlug] = Field(default_factory=list)
    images: list[PortfolioImageRead] = Field(default_factory=list)
