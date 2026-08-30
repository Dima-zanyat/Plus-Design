"""Просмотр и обработка заявок для администратора."""

from fastapi import APIRouter, Depends, status

from app.api.deps import LeadServiceDep, get_current_admin
from app.dependencies import Pagination
from app.schemas.common import ErrorResponse, Page
from app.schemas.lead import LeadRead, LeadStatusUpdate

router = APIRouter(
    prefix="/admin",
    tags=["admin-leads"],
    dependencies=[Depends(get_current_admin)],
)


@router.get(
    "/leads",
    response_model=Page[LeadRead],
    summary="Список заявок, новые сверху",
)
async def list_leads(
    service: LeadServiceDep,
    pagination: Pagination,
) -> Page[LeadRead]:
    return await service.list_leads(pagination)


@router.patch(
    "/leads/{lead_id}",
    response_model=LeadRead,
    summary="Изменить статус заявки",
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}},
)
async def update_lead_status(
    lead_id: int,
    payload: LeadStatusUpdate,
    service: LeadServiceDep,
) -> LeadRead:
    return await service.update_status(lead_id, payload.status)
