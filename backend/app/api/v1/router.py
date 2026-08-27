"""Агрегирующий роутер /api/v1."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, leads, portfolio

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(portfolio.router)
api_router.include_router(leads.router)
