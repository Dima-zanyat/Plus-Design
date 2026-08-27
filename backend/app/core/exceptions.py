"""Доменные исключения.

Слой домена и сервисов не знает про HTTP: он бросает эти исключения,
а транспортный слой (FastAPI) превращает их в HTTP-ответы.
"""


class DomainError(Exception):
    """Базовое доменное исключение."""

    message: str = "Внутренняя ошибка домена"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.message
        super().__init__(self.message)


class NotFoundError(DomainError):
    """Сущность не найдена."""

    message = "Ресурс не найден"


class ValidationError(DomainError):
    """Нарушено бизнес-правило."""

    message = "Некорректные данные"


class ConflictError(DomainError):
    """Конфликт состояния (например, дубликат уникального поля)."""

    message = "Конфликт данных"


class UnauthorizedError(DomainError):
    """Нет прав или неверные учётные данные."""

    message = "Нужна авторизация"
