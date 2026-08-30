"""Загрузка изображений для портфолио (обложка, галерея). Только администратор."""

import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, status

from app.api.deps import get_current_admin
from app.config import get_settings
from app.core.exceptions import ValidationError
from app.schemas.common import ErrorResponse
from app.schemas.media import UploadedFile

router = APIRouter(
    prefix="/admin",
    tags=["admin-media"],
    dependencies=[Depends(get_current_admin)],
)

_ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}
_MAX_UPLOAD_BYTES = 8 * 1024 * 1024  # 8 МБ


@router.post(
    "/media/upload",
    response_model=UploadedFile,
    status_code=status.HTTP_201_CREATED,
    summary="Загрузить изображение (обложка или кадр галереи)",
    responses={422: {"model": ErrorResponse}},
)
async def upload_image(file: UploadFile) -> UploadedFile:
    """Принимает multipart-файл, сохраняет в `media_root`, возвращает публичный URL."""
    extension = _ALLOWED_CONTENT_TYPES.get(file.content_type or "")
    if extension is None:
        raise ValidationError("Поддерживаются только изображения: JPEG, PNG, WEBP, GIF")

    body = await file.read()
    if not body:
        raise ValidationError("Пустой файл")
    if len(body) > _MAX_UPLOAD_BYTES:
        raise ValidationError("Файл слишком большой: максимум 8 МБ")

    settings = get_settings()
    settings.media_root.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{extension}"
    destination: Path = settings.media_root / filename
    destination.write_bytes(body)

    url = f"{settings.media_url_prefix.rstrip('/')}/{filename}"
    return UploadedFile(url=url)
