"""Расширить схему портфолио до текущей модели."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_expand_portfolio"
down_revision: str | None = "0001_init"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("slug", sa.String(length=140), nullable=False),
    )
    op.create_index("ix_categories_slug", "categories", ["slug"], unique=True)

    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
    )
    op.create_index("ix_tags_slug", "tags", ["slug"], unique=True)

    op.add_column(
        "portfolio_items",
        sa.Column("is_published", sa.Boolean(), server_default=sa.true(), nullable=False),
    )
    op.add_column(
        "portfolio_items",
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
    )
    op.add_column(
        "portfolio_items",
        sa.Column(
            "category_id",
            sa.Integer(),
            sa.ForeignKey("categories.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_portfolio_items_published_sort",
        "portfolio_items",
        ["is_published", "sort_order", sa.text("created_at DESC"), sa.text("id DESC")],
    )

    op.create_table(
        "portfolio_images",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column(
            "item_id",
            sa.Integer(),
            sa.ForeignKey("portfolio_items.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("alt", sa.String(length=200), server_default="", nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
    )
    op.create_index("ix_portfolio_images_item_id", "portfolio_images", ["item_id"])

    op.create_table(
        "portfolio_item_tags",
        sa.Column(
            "item_id",
            sa.Integer(),
            sa.ForeignKey("portfolio_items.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "tag_id",
            sa.Integer(),
            sa.ForeignKey("tags.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("portfolio_item_tags")
    op.drop_index("ix_portfolio_images_item_id", table_name="portfolio_images")
    op.drop_table("portfolio_images")
    op.drop_index("ix_portfolio_items_published_sort", table_name="portfolio_items")
    op.drop_column("portfolio_items", "category_id")
    op.drop_column("portfolio_items", "sort_order")
    op.drop_column("portfolio_items", "is_published")
    op.drop_index("ix_tags_slug", table_name="tags")
    op.drop_table("tags")
    op.drop_index("ix_categories_slug", table_name="categories")
    op.drop_table("categories")
