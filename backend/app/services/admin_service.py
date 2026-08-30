from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, credentials_match
from app.schemas.auth import LoginRequest, TokenResponse


class AdminService:
    async def get_access(self, payload: LoginRequest) -> TokenResponse:
        if not credentials_match(payload.username, payload.password):
            raise UnauthorizedError("Неверные учётные данные")
        return TokenResponse(access_token=create_access_token(subject=payload.username))
