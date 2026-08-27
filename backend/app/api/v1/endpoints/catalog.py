"""Публичные справочники витрины."""

from fastapi import APIRouter

from app.api.deps import PortfolioServiceDep
from app.schemas.portfolio import NamedSlug

router = APIRouter(tags=["catalog"])


@router.get("/categories", response_model=list[NamedSlug], summary="Категории портфолио")
async def list_categories(service: PortfolioServiceDep) -> list[NamedSlug]:
    return await service.list_categories()


@router.get("/tags", response_model=list[NamedSlug], summary="Теги портфолио")
async def list_tags(service: PortfolioServiceDep) -> list[NamedSlug]:
    return await service.list_tags()
