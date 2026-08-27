"""Модель заявки на проект."""

import enum

from sqlalchemy import Enum as SAEnum
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class LeadStatus(enum.StrEnum):
    """Стадия обработки заявки."""

    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    REJECTED = "rejected"


class Lead(Base, TimestampMixin):
    """Заявка на проект, оставленная через форму на сайте."""

    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(254), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[LeadStatus] = mapped_column(
        SAEnum(
            LeadStatus,
            name="lead_status",
            native_enum=True,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        default=LeadStatus.NEW,
        server_default=LeadStatus.NEW.value,
    )

    def __repr__(self) -> str:  # pragma: no cover - отладочное представление
        return f"<Lead id={self.id} phone={self.phone!r} status={self.status.value}>"
