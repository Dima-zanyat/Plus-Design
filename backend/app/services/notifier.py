"""Уведомления о новой заявке: почта и/или Telegram."""

from email.message import EmailMessage

import httpx
from aiosmtplib import SMTP

from app.config import Settings
from app.core.logging import get_logger
from app.schemas.lead import LeadRead

logger = get_logger(__name__)


class LeadNotifier:
    """Отправляет уведомление, если настроен хотя бы один канал.

    Ошибки канала не роняют приём заявки.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def notify_new_lead(self, lead: LeadRead) -> None:
        text = (
            f"Новая заявка #{lead.id}\n"
            f"Имя: {lead.name}\n"
            f"Телефон: {lead.phone}\n"
            f"Email: {lead.email or '—'}\n"
            f"Сообщение: {lead.message or '—'}"
        )
        sent: bool = False
        if self._settings.telegram_bot_token and self._settings.telegram_chat_id:
            sent = await self._telegram(text) or sent
        if (
            self._settings.smtp_host
            and self._settings.smtp_to
            and self._settings.smtp_from
        ):
            sent = await self._email(text) or sent
        if not sent:
            logger.info("Заявка id=%s принята, канал уведомлений не настроен", lead.id)

    async def _telegram(self, text: str) -> bool:
        url = f"https://api.telegram.org/bot{self._settings.telegram_bot_token}/sendMessage"
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    url,
                    json={
                        "chat_id": self._settings.telegram_chat_id,
                        "text": text,
                    },
                )
                response.raise_for_status()
            return True
        except Exception:
            logger.exception("Не удалось отправить заявку в Telegram")
            return False

    async def _email(self, text: str) -> bool:
        message = EmailMessage()
        message["From"] = self._settings.smtp_from or ""
        message["To"] = self._settings.smtp_to or ""
        message["Subject"] = "Плюс Дизайн: новая заявка"
        message.set_content(text)
        try:
            smtp = SMTP(
                hostname=self._settings.smtp_host,
                port=self._settings.smtp_port,
                start_tls=self._settings.smtp_starttls,
            )
            await smtp.connect()
            if self._settings.smtp_user and self._settings.smtp_password:
                await smtp.login(self._settings.smtp_user, self._settings.smtp_password)
            await smtp.send_message(message)
            await smtp.quit()
            return True
        except Exception:
            logger.exception("Не удалось отправить заявку по почте")
            return False
