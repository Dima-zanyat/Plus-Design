"""Зависимости API-слоя: сборка сервисов и админ."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import Settings, get_settings
from app.core.exceptions import UnauthorizedError
from app.core.security import decode_subject
from app.dependencies import DbSession
from app.repositories.catalog_repo import CategoryRepository, TagRepository
from app.repositories.lead_repo import LeadRepository
from app.repositories.portfolio_repo import PortfolioRepository
from app.services.admin_service import AdminService
from app.services.lead_service import LeadService
from app.services.notifier import LeadNotifier
from app.services.portfolio_service import PortfolioService

_bearer = HTTPBearer(auto_error=False)


def get_portfolio_service(session: DbSession) -> PortfolioService:
    return PortfolioService(
        PortfolioRepository(session),
        CategoryRepository(session),
        TagRepository(session),
    )


def get_admin_service() -> AdminService:
    return AdminService()


def get_lead_service(session: DbSession) -> LeadService:
    return LeadService(LeadRepository(session))


def get_notifier(settings: Annotated[Settings, Depends(get_settings)]) -> LeadNotifier:
    return LeadNotifier(settings)


def get_current_admin(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> str:
    if credentials is None:
        raise UnauthorizedError("Нужна авторизация")
    username = decode_subject(credentials.credentials)
    if username != settings.admin_username:
        raise UnauthorizedError("Нужна авторизация")
    return username


PortfolioServiceDep = Annotated[PortfolioService, Depends(get_portfolio_service)]
LeadServiceDep = Annotated[LeadService, Depends(get_lead_service)]
AdminServiceDep = Annotated[AdminService, Depends(get_admin_service)]
NotifierDep = Annotated[LeadNotifier, Depends(get_notifier)]
AdminUser = Annotated[str, Depends(get_current_admin)]
