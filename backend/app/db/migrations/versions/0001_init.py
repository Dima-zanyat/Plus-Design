"""Начальная схема: портфолио и заявки."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_init"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "portfolio_items",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=220), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("cover_image", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_portfolio_items_slug", "portfolio_items", ["slug"], unique=True)
    op.create_index(
        "ix_portfolio_items_created_at_id",
        "portfolio_items",
        [sa.text("created_at DESC"), sa.text("id DESC")],
    )

    lead_status = postgresql.ENUM(
        "new", "in_progress", "done", "rejected", name="lead_status", create_type=False
    )
    lead_status.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "leads",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=True),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("status", lead_status, server_default="new", nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_leads_phone", "leads", ["phone"])


def downgrade() -> None:
    op.drop_index("ix_leads_phone", table_name="leads")
    op.drop_table("leads")
    postgresql.ENUM(name="lead_status").drop(op.get_bind(), checkfirst=True)
    op.drop_index("ix_portfolio_items_created_at_id", table_name="portfolio_items")
    op.drop_index("ix_portfolio_items_slug", table_name="portfolio_items")
    op.drop_table("portfolio_items")
