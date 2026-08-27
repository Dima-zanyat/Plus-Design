"""Pydantic-схемы заявки на проект."""

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.lead import LeadStatus

_PHONE_ALLOWED = re.compile(r"^\+?[\d\s\-()]{7,25}$")
_NON_DIGITS = re.compile(r"\D")


class LeadCreate(BaseModel):
    """Тело формы-заявки на проект.

    Обязательны имя и телефон, email — опционален.
    """

    name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=7, max_length=25)
    email: EmailStr | None = None
    message: str | None = Field(default=None, max_length=2000)

    @field_validator("name")
    @classmethod
    def _strip_name(cls, value: str) -> str:
        cleaned = " ".join(value.split())
        if len(cleaned) < 2:
            raise ValueError("Имя должно содержать минимум 2 символа")
        return cleaned

    @field_validator("phone")
    @classmethod
    def _normalize_phone(cls, value: str) -> str:
        """Привести телефон к виду `+<цифры>` (E.164-совместимому)."""
        raw = value.strip()
        if not _PHONE_ALLOWED.match(raw):
            raise ValueError("Телефон содержит недопустимые символы")

        digits = _NON_DIGITS.sub("", raw)
        # Российские номера в записи 8XXXXXXXXXX приводим к +7XXXXXXXXXX.
        if len(digits) == 11 and digits.startswith("8"):
            digits = "7" + digits[1:]
        if not 10 <= len(digits) <= 15:
            raise ValueError("Телефон должен содержать от 10 до 15 цифр")
        return f"+{digits}"

    @field_validator("message")
    @classmethod
    def _strip_message(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None


class LeadStatusUpdate(BaseModel):
    status: LeadStatus


class LeadRead(BaseModel):
    """Представление заявки в ответах API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    email: str | None
    message: str | None
    status: LeadStatus
    created_at: datetime
