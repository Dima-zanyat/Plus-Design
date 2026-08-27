"""Эндпоинты формы-заявки на проект."""

from fastapi import APIRouter, status

from app.api.deps import LeadServiceDep
from app.schemas.common import ErrorResponse
from app.schemas.lead import LeadCreate, LeadRead

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post(
    "",
    response_model=LeadRead,
    status_code=status.HTTP_201_CREATED,
    summary="Отправить заявку на проект",
    responses={
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def create_lead(
    payload: LeadCreate,
    service: LeadServiceDep,
) -> LeadRead:
    """Принять заявку: имя и телефон обязательны, email опционален."""
    return await service.submit(payload)
