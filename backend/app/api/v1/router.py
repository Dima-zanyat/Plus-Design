"""Агрегирующий роутер /api/v1."""

from fastapi import APIRouter

from app.api.v1.endpoints import admin, admin_portfolio, catalog, health, leads, portfolio

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(catalog.router)
api_router.include_router(portfolio.router)
api_router.include_router(leads.router)
api_router.include_router(admin.auth_router)
api_router.include_router(admin.protected_router)
api_router.include_router(admin_portfolio.router)
