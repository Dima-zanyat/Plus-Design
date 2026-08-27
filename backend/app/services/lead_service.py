"""Бизнес-логика заявок на проект."""

from datetime import timedelta
from typing import Protocol

from app.core.exceptions import ConflictError, NotFoundError
from app.core.logging import get_logger
from app.models.lead import Lead, LeadStatus
from app.schemas.common import Page, PaginationParams
from app.schemas.lead import LeadCreate, LeadRead

logger = get_logger(__name__)

#: Окно антидубля: повторная заявка с того же телефона отклоняется.
DUPLICATE_WINDOW = timedelta(minutes=5)


class LeadRepositoryProtocol(Protocol):
    """Контракт хранилища заявок."""

    async def count_recent_by_phone(self, phone: str, within: timedelta) -> int: ...

    async def add(self, entity: Lead) -> Lead: ...

    async def get(self, entity_id: int) -> Lead | None: ...

    async def list_paginated(self, offset: int, limit: int) -> tuple[list[Lead], int]: ...


class LeadService:
    """Сценарии обработки формы-заявки."""

    def __init__(self, repository: LeadRepositoryProtocol) -> None:
        self._repository = repository

    async def submit(self, payload: LeadCreate) -> LeadRead:
        """Принять заявку с сайта.

        Телефон уже нормализован на уровне схемы, поэтому проверка
        дубликата работает по каноническому виду номера.
        """
        recent = await self._repository.count_recent_by_phone(
            payload.phone, DUPLICATE_WINDOW
        )
        if recent:
            raise ConflictError(
                "Заявка с этим номером уже принята. Мы скоро свяжемся с вами."
            )

        lead = Lead(
            name=payload.name,
            phone=payload.phone,
            email=payload.email,
            message=payload.message,
        )
        await self._repository.add(lead)
        logger.info("Принята новая заявка id=%s", lead.id)
        return LeadRead.model_validate(lead)

    async def list_leads(self, pagination: PaginationParams) -> Page[LeadRead]:
        items, total = await self._repository.list_paginated(
            offset=pagination.offset, limit=pagination.limit
        )
        return Page.create(
            items=[LeadRead.model_validate(item) for item in items],
            total=total,
            page=pagination.page,
            size=pagination.size,
        )

    async def update_status(self, lead_id: int, status: LeadStatus) -> LeadRead:
        lead = await self._repository.get(lead_id)
        if lead is None:
            raise NotFoundError(f"Заявка с id {lead_id} не найдена")
        lead.status = status
        return LeadRead.model_validate(lead)
