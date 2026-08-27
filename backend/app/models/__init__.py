"""Модели БД.

Импорт всех моделей здесь регистрирует их в `Base.metadata` —
это нужно Alembic для автогенерации и тестам для `create_all`.
"""

from app.models.lead import Lead, LeadStatus
from app.models.portfolio import Category, PortfolioImage, PortfolioItem, Tag

__all__ = [
    "Category",
    "Lead",
    "LeadStatus",
    "PortfolioImage",
    "PortfolioItem",
    "Tag",
]
