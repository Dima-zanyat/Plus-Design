"""Настройки приложения из переменных окружения."""

from functools import lru_cache
from pathlib import Path
from typing import Literal, Self

from pydantic import Field, PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения.

    Значения читаются из переменных окружения или файла `.env`.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Приложение ---
    app_name: str = "PlusDesign API"
    environment: Literal["local", "test", "staging", "production"] = "local"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    # --- База данных ---
    database_url: str = Field(
        default="postgresql+asyncpg://plusdesign:plusdesign@db:5432/plusdesign",
        alias="DATABASE_URL",
    )
    db_echo: bool = False
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_pre_ping: bool = True

    # --- CORS ---
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # --- Пагинация ---
    default_page_size: int = 12
    max_page_size: int = 100

    # --- Логирование ---
    log_level: str = "INFO"

    # --- Авторизация ---
    jwt_secret: str = "dev-only-change-me"
    jwt_expire_minutes: int = 60 * 24
    admin_username: str = "admin"
    admin_password: str = "admin"

    # --- Медиа ---
    media_root: Path = Path("media")
    media_url_prefix: str = "/media"

    # --- Уведомления о заявках ---
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None
    smtp_to: str | None = None
    smtp_starttls: bool = True
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None

    @property
    def database_url_str(self) -> str:
        return str(self.database_url)

    @model_validator(mode="after")
    def _require_prod_secrets(self) -> Self:
        if self.environment == "production":
            if self.jwt_secret in {"", "dev-only-change-me"}:
                raise ValueError("JWT_SECRET обязателен в production")
            if self.admin_password in {"", "admin"}:
                raise ValueError("ADMIN_PASSWORD должен быть задан в production")
        return self


@lru_cache
def get_settings() -> Settings:
    """Кэшированный доступ к настройкам."""
    return Settings()


settings = get_settings()
