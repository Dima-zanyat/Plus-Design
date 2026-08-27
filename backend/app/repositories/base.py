"""Базовый асинхронный репозиторий."""

from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Общая обвязка над сессией SQLAlchemy.

    Репозиторий не коммитит транзакцию — этим управляет сервисный слой,
    чтобы одна бизнес-операция оставалась одной транзакцией.
    """

    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session

    async def add(self, entity: ModelT) -> ModelT:
        self._session.add(entity)
        await self._session.flush()
        return entity

    async def get(self, entity_id: int) -> ModelT | None:
        return await self._session.get(self.model, entity_id)
