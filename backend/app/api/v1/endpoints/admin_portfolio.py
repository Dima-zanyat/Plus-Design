"""CRUD портфолио, категорий и тегов для администратора."""

from fastapi import APIRouter, Depends, status

from app.api.deps import PortfolioServiceDep, get_current_admin
from app.dependencies import Pagination
from app.schemas.common import ErrorResponse, Page
from app.schemas.portfolio import (
    NamedSlug,
    NamedSlugCreate,
    PortfolioItemCreate,
    PortfolioItemRead,
    PortfolioItemUpdate,
)

router = APIRouter(
    prefix="/admin",
    tags=["admin-portfolio"],
    dependencies=[Depends(get_current_admin)],
)


@router.get(
    "/portfolio",
    response_model=Page[PortfolioItemRead],
    summary="Все работы, включая черновики",
)
async def list_admin_portfolio(
    service: PortfolioServiceDep,
    pagination: Pagination,
) -> Page[PortfolioItemRead]:
    return await service.list_items(pagination, published_only=False)


@router.post(
    "/portfolio",
    response_model=PortfolioItemRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать работу",
    responses={status.HTTP_409_CONFLICT: {"model": ErrorResponse}},
)
async def create_portfolio_item(
    payload: PortfolioItemCreate,
    service: PortfolioServiceDep,
) -> PortfolioItemRead:
    return await service.create(payload=payload)


@router.get(
    "/portfolio/{item_id}",
    response_model=PortfolioItemRead,
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}},
)
async def get_admin_portfolio_item(
    item_id: int,
    service: PortfolioServiceDep,
) -> PortfolioItemRead:
    return await service.get_by_id(item_id)


@router.patch(
    "/portfolio/{item_id}",
    response_model=PortfolioItemRead,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
async def update_portfolio_item(
    item_id: int,
    payload: PortfolioItemUpdate,
    service: PortfolioServiceDep,
) -> PortfolioItemRead:
    return await service.update(item_id, payload)


@router.delete(
    "/portfolio/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}},
)
async def delete_portfolio_item(
    item_id: int,
    service: PortfolioServiceDep,
) -> None:
    await service.delete(item_id)


@router.post(
    "/categories",
    response_model=NamedSlug,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    payload: NamedSlugCreate,
    service: PortfolioServiceDep,
) -> NamedSlug:
    return await service.create_category(payload)


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(category_id: int, service: PortfolioServiceDep) -> None:
    await service.delete_category(category_id)


@router.post(
    "/tags",
    response_model=NamedSlug,
    status_code=status.HTTP_201_CREATED,
)
async def create_tag(
    payload: NamedSlugCreate,
    service: PortfolioServiceDep,
) -> NamedSlug:
    return await service.create_tag(payload)


@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, service: PortfolioServiceDep) -> None:
    await service.delete_tag(tag_id)
