"""Тесты загрузки изображений в админке."""

import pytest
from httpx import AsyncClient

from app.config import settings

pytestmark = pytest.mark.asyncio

# Валидный однопиксельный PNG.
_TINY_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000010802000000907724"
    "6e0000000c4944415478da6360606060000000050001a5f645400000000049454e44ae426082"
)


async def _auth_headers(client: AsyncClient) -> dict[str, str]:
    login = await client.post(
        "/api/v1/admin/login",
        json={"username": settings.admin_username, "password": settings.admin_password},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


async def test_upload_requires_auth(client: AsyncClient) -> None:
    files = {"file": ("cover.png", _TINY_PNG, "image/png")}
    response = await client.post("/api/v1/admin/media/upload", files=files)
    assert response.status_code == 401


async def test_upload_returns_url(client: AsyncClient) -> None:
    headers = await _auth_headers(client)
    files = {"file": ("cover.png", _TINY_PNG, "image/png")}
    response = await client.post(
        "/api/v1/admin/media/upload", files=files, headers=headers
    )
    assert response.status_code == 201
    body = response.json()
    assert body["url"].startswith("/media/")
    assert body["url"].endswith(".png")


async def test_upload_rejects_unknown_content_type(client: AsyncClient) -> None:
    headers = await _auth_headers(client)
    files = {"file": ("evil.exe", b"not-an-image", "application/octet-stream")}
    response = await client.post(
        "/api/v1/admin/media/upload", files=files, headers=headers
    )
    assert response.status_code == 422


async def test_uploaded_url_can_be_used_as_cover(client: AsyncClient) -> None:
    headers = await _auth_headers(client)
    files = {"file": ("cover.png", _TINY_PNG, "image/png")}
    uploaded = await client.post(
        "/api/v1/admin/media/upload", files=files, headers=headers
    )
    url = uploaded.json()["url"]

    created = await client.post(
        "/api/v1/admin/portfolio",
        json={"title": "С загруженной обложкой", "slug": "s-oblozhkoy", "cover_image": url},
        headers=headers,
    )
    assert created.status_code == 201
    assert created.json()["cover_image"] == url
