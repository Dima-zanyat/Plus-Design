"""Схема ответа на загрузку файла."""

from pydantic import BaseModel


class UploadedFile(BaseModel):
    url: str
