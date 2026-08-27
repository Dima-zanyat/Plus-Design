"""Восстановить обязательные колонки портфолио в существующих базах."""

from collections.abc import Sequence

from alembic import op

revision: str = "0003_repair_portfolio_columns"
down_revision: str | None = "0002_expand_portfolio"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE portfolio_items "
        "ADD COLUMN IF NOT EXISTS is_published BOOLEAN DEFAULT true NOT NULL"
    )
    op.execute(
        "ALTER TABLE portfolio_items "
        "ADD COLUMN IF NOT EXISTS sort_order INTEGER DEFAULT 0 NOT NULL"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_portfolio_items_published_sort "
        "ON portfolio_items (is_published, sort_order, created_at DESC, id DESC)"
    )


def downgrade() -> None:
    op.execute(
        "DROP INDEX IF EXISTS ix_portfolio_items_published_sort"
    )
    op.execute("ALTER TABLE portfolio_items DROP COLUMN IF EXISTS sort_order")
    op.execute("ALTER TABLE portfolio_items DROP COLUMN IF EXISTS is_published")
