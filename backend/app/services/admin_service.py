from app.dependencies import AppSettings
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, TokenResponse


class AdminService:

    def __init__(self, settings: AppSettings) -> None:
        self._settings = settings

    async def get_access(self, payload: LoginRequest) -> TokenResponse:
        """Получение доступа JWT-токена."""
        if payload.username != self._settings.admin_username:
            raise ValueError("Неверный username.")
        if payload.password != self._settings.admin_password:
            raise ValueError("Неверный пароль.")
        access_token: str = create_access_token(subject=payload.username)
        return TokenResponse(access_token=access_token)
