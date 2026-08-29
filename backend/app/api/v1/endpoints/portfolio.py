"""Эндпоинты портфолио (публичная витрина)."""

from typing import Annotated

from fastapi import APIRouter, Query, status, Depends

from app.api.deps import PortfolioServiceDep, get_current_admin
from app.dependencies import Pagination
from app.schemas.common import ErrorResponse, Page
from app.schemas.portfolio import (
    NamedSlug,
    NamedSlugCreate,
    NamedSlugUpdate,
    PortfolioImageIn,
    PortfolioItemCreate,
    PortfolioItemRead,
    PortfolioItemUpdate,
)

router = APIRouter(prefix="/portfolio", tags=["portfolio"])
admin_router = APIRouter(
    prefix="/portfolio",
    tags=["admin-portfolio"],
    dependencies=[Depends(get_current_admin)],
)


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


# Создание сущностей


@admin_router.post("/create/portfolio", response_model=PortfolioItemRead)
async def create_portfolio_item(
    payload: PortfolioItemCreate,
    service: PortfolioServiceDep,
):
    return await service.create(payload=payload)


@admin_router.post("/create/category", response_model=NamedSlug)
async def create_category(
    payload: NamedSlugCreate,
    service: PortfolioServiceDep,
) -> NamedSlug:
    return await service.create_category(payload)


@admin_router.post("/create/tag", response_model=NamedSlug)
async def create_tag(
    payload: NamedSlugCreate, service: PortfolioServiceDep
) -> NamedSlug:
    return await service.create_tag(payload)


# Удаление сущностей


@admin_router.delete(
    "/delete/portfolio/{item_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_portfolio_item(
    item_id: int,
    service: PortfolioServiceDep,
) -> None:
    await service.delete(item_id)


@admin_router.delete(
    "/delete/category/{category_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(category_id: int, service: PortfolioServiceDep) -> None:
    await service.delete_category(category_id)


@admin_router.delete("/delete/tag/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, service: PortfolioServiceDep) -> None:
    await service.delete_tag(tag_id)
