"""JWT и сравнение пароля администратора."""

from datetime import UTC, datetime, timedelta

import jwt

from app.config import settings
from app.core.exceptions import UnauthorizedError

ALGORITHM = "HS256"


def create_access_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode(
        {"sub": subject, "exp": expire},
        settings.jwt_secret,
        algorithm=ALGORITHM,
    )


def decode_subject(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise UnauthorizedError("Недействительный токен") from exc
    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise UnauthorizedError("Недействительный токен")
    return subject


def credentials_match(username: str, password: str) -> bool:
    return username == settings.admin_username and password == settings.admin_password
