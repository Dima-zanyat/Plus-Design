"""Модели портфолио: работы, категории, теги, галерея."""

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
    text,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

portfolio_item_tags = Table(
    "portfolio_item_tags",
    Base.metadata,
    Column(
        "item_id",
        ForeignKey("portfolio_items.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Category(Base):
    """Категория работ (квартира, дом и т.п.)."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(140),
        nullable=False,
        unique=True,
        index=True,
    )

    items: Mapped[list["PortfolioItem"]] = relationship(
        back_populates="category",
        lazy="selectin",
    )


class Tag(Base):
    """Тег работы."""

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    items: Mapped[list["PortfolioItem"]] = relationship(
        secondary=portfolio_item_tags,
        back_populates="tags",
        lazy="selectin",
    )


class PortfolioImage(Base):
    """Кадр галереи проекта."""

    __tablename__ = "portfolio_images"

    id: Mapped[int] = mapped_column(primary_key=True)

    item_id: Mapped[int] = mapped_column(
        ForeignKey("portfolio_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    alt: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        default="",
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    item: Mapped["PortfolioItem"] = relationship(
        back_populates="images",
        lazy="selectin",
    )


class PortfolioItem(Base, TimestampMixin):
    """Работа в портфолио: карточка в витрине и страница проекта."""

    __tablename__ = "portfolio_items"

    __table_args__ = (
        Index(
            "ix_portfolio_items_published_sort",
            "is_published",
            "sort_order",
            text("created_at DESC"),
            text("id DESC"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(220),
        nullable=False,
        unique=True,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    cover_image: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_published: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=true(),
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "categories.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    category: Mapped[Category | None] = relationship(
        back_populates="items",
        lazy="selectin",
    )

    tags: Mapped[list[Tag]] = relationship(
        secondary=portfolio_item_tags,
        back_populates="items",
        lazy="selectin",
    )

    images: Mapped[list[PortfolioImage]] = relationship(
        back_populates="item",
        cascade="all, delete-orphan",
        order_by="PortfolioImage.sort_order",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<PortfolioItem id={self.id} slug={self.slug!r}>"
