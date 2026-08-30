"""Тесты авторизации и админского CRUD."""

import pytest
from httpx import AsyncClient

from app.config import settings

pytestmark = pytest.mark.asyncio


def _login_body() -> dict[str, str]:
    return {
        "username": settings.admin_username,
        "password": settings.admin_password,
    }


async def test_login_success(client: AsyncClient) -> None:
    response = await client.post("/api/v1/admin/login", json=_login_body())
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


async def test_login_rejects_bad_password(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/admin/login",
        json={"username": settings.admin_username, "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверные учётные данные"


async def test_login_rejects_unknown_user(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/admin/login",
        json={"username": "not-admin", "password": settings.admin_password},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверные учётные данные"


async def test_admin_portfolio_requires_token(client: AsyncClient) -> None:
    response = await client.get("/api/v1/admin/portfolio")
    assert response.status_code == 401


async def test_admin_crud_roundtrip(client: AsyncClient) -> None:
    login = await client.post("/api/v1/admin/login", json=_login_body())
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    created = await client.post(
        "/api/v1/admin/portfolio",
        json={
            "title": "Квартира на Садовой",
            "slug": "kvartira-sadovaya",
            "description": "Планировка и визуализация.",
            "cover_image": "https://example.com/cover.jpg",
            "images": [{"url": "https://example.com/1.jpg", "alt": "Гостиная"}],
        },
        headers=headers,
    )
    assert created.status_code == 201
    item_id = created.json()["id"]

    me = await client.get("/api/v1/admin/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["username"] == settings.admin_username

    listed = await client.get("/api/v1/admin/portfolio", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["total"] == 1

    fetched = await client.get(f"/api/v1/admin/portfolio/{item_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["images"][0]["url"] == "https://example.com/1.jpg"

    patched = await client.patch(
        f"/api/v1/admin/portfolio/{item_id}",
        json={"title": "Квартира обновлена", "is_published": True},
        headers=headers,
    )
    assert patched.status_code == 200
    assert patched.json()["title"] == "Квартира обновлена"

    deleted = await client.delete(
        f"/api/v1/admin/portfolio/{item_id}",
        headers=headers,
    )
    assert deleted.status_code == 204
    assert (await client.get("/api/v1/portfolio/kvartira-sadovaya")).status_code == 404


async def test_admin_lists_unpublished(client: AsyncClient) -> None:
    login = await client.post("/api/v1/admin/login", json=_login_body())
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    created = await client.post(
        "/api/v1/admin/portfolio",
        json={"title": "Черновик", "slug": "draft-item", "is_published": False},
        headers=headers,
    )
    assert created.status_code == 201
    listed = await client.get("/api/v1/admin/portfolio", headers=headers)
    assert listed.json()["total"] == 1
    assert listed.json()["items"][0]["is_published"] is False
    assert (await client.get("/api/v1/portfolio")).json()["total"] == 0


async def test_admin_category_and_tag_crud(client: AsyncClient) -> None:
    login = await client.post("/api/v1/admin/login", json=_login_body())
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    category = await client.post(
        "/api/v1/admin/categories",
        json={"name": "Квартира", "slug": "kvartira"},
        headers=headers,
    )
    assert category.status_code == 201
    tag = await client.post(
        "/api/v1/admin/tags",
        json={"name": "Визуализация", "slug": "vizualizaciya"},
        headers=headers,
    )
    assert tag.status_code == 201

    catalog = await client.get("/api/v1/categories")
    assert catalog.status_code == 200
    assert catalog.json()[0]["slug"] == "kvartira"

    assert (
        await client.delete(
            f"/api/v1/admin/tags/{tag.json()['id']}",
            headers=headers,
        )
    ).status_code == 204
    assert (
        await client.delete(
            f"/api/v1/admin/categories/{category.json()['id']}",
            headers=headers,
        )
    ).status_code == 204
