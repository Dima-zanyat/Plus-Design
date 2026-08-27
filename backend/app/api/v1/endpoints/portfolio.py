"""Эндпоинты портфолио (публичная витрина)."""

from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.deps import PortfolioServiceDep
from app.dependencies import Pagination
from app.schemas.common import ErrorResponse, Page
from app.schemas.portfolio import PortfolioItemCreate, PortfolioItemRead

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get(
    "",
    response_model=Page[PortfolioItemRead],
    summary="Список опубликованных работ с пагинацией и фильтрами",
)
async def list_portfolio(
    service: PortfolioServiceDep,
    pagination: Pagination,
    category: Annotated[str | None, Query(description="Slug категории")] = None,
    tag: Annotated[str | None, Query(description="Slug тега")] = None,
) -> Page[PortfolioItemRead]:
    """Только опубликованные работы, порядок: sort_order, затем новые."""
    return await service.list_items(
        pagination,
        published_only=True,
        category_slug=category,
        tag_slug=tag,
    )


@router.post(
    "",
    response_model=PortfolioItemRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать работу портфолио",
    responses={status.HTTP_409_CONFLICT: {"model": ErrorResponse}},
)
async def create_portfolio_item(
    payload: PortfolioItemCreate,
    service: PortfolioServiceDep,
) -> PortfolioItemRead:
    """Создать работу портфолио."""
    return await service.create(payload)


@router.get(
    "/{slug}",
    response_model=PortfolioItemRead,
    summary="Опубликованная работа по slug",
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}},
)
async def get_portfolio_item(
    slug: str,
    service: PortfolioServiceDep,
) -> PortfolioItemRead:
    return await service.get_by_slug(slug, published_only=True)
