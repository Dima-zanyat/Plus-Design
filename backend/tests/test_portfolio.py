"""Тесты эндпоинтов портфолио."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.portfolio import PortfolioItem

pytestmark = pytest.mark.asyncio


async def _seed(session: AsyncSession, count: int) -> None:
    for i in range(count):
        session.add(
            PortfolioItem(
                title=f"Работа {i}",
                slug=f"rabota-{i}",
                description=f"Описание {i}",
                cover_image=f"/media/{i}.jpg",
            )
        )
    await session.commit()


async def _auth_headers(client: AsyncClient) -> dict[str, str]:
    response = await client.post(
        "/api/v1/admin/login",
        json={"username": settings.admin_username, "password": settings.admin_password},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def test_empty_portfolio_returns_empty_page(client: AsyncClient) -> None:
    response = await client.get("/api/v1/portfolio")
    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["total"] == 0
    assert body["pages"] == 0
    assert body["has_next"] is False
    assert body["has_prev"] is False


async def test_pagination_slices_results(
    client: AsyncClient, session: AsyncSession
) -> None:
    await _seed(session, 25)

    first = (await client.get("/api/v1/portfolio", params={"page": 1, "size": 10})).json()
    assert len(first["items"]) == 10
    assert first["total"] == 25
    assert first["pages"] == 3
    assert first["has_next"] is True
    assert first["has_prev"] is False

    last = (await client.get("/api/v1/portfolio", params={"page": 3, "size": 10})).json()
    assert len(last["items"]) == 5
    assert last["has_next"] is False
    assert last["has_prev"] is True

    first_slugs = {item["slug"] for item in first["items"]}
    last_slugs = {item["slug"] for item in last["items"]}
    assert not first_slugs & last_slugs


async def test_pagination_rejects_bad_params(client: AsyncClient) -> None:
    assert (await client.get("/api/v1/portfolio", params={"page": 0})).status_code == 422
    assert (await client.get("/api/v1/portfolio", params={"size": 500})).status_code == 422


async def test_public_create_is_closed(client: AsyncClient) -> None:
    payload = {
        "title": "Айдентика кофейни",
        "slug": "aydentika-kofeyni",
        "description": "Логотип, упаковка, вывеска.",
        "cover_image": "/media/coffee.jpg",
    }
    created = await client.post("/api/v1/portfolio", json=payload)
    assert created.status_code == 405


async def test_create_and_get_by_slug(client: AsyncClient) -> None:
    payload = {
        "title": "Айдентика кофейни",
        "slug": "aydentika-kofeyni",
        "description": "Логотип, упаковка, вывеска.",
        "cover_image": "/media/coffee.jpg",
    }
    headers = await _auth_headers(client)
    created = await client.post("/api/v1/admin/portfolio", json=payload, headers=headers)
    assert created.status_code == 201
    assert created.json()["slug"] == payload["slug"]

    fetched = await client.get(f"/api/v1/portfolio/{payload['slug']}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == payload["title"]


async def test_duplicate_slug_conflicts(client: AsyncClient) -> None:
    payload = {"title": "Один", "slug": "odin", "description": ""}
    headers = await _auth_headers(client)
    assert (
        await client.post("/api/v1/admin/portfolio", json=payload, headers=headers)
    ).status_code == 201
    assert (
        await client.post("/api/v1/admin/portfolio", json=payload, headers=headers)
    ).status_code == 409


async def test_unknown_slug_returns_404(client: AsyncClient) -> None:
    response = await client.get("/api/v1/portfolio/net-takoy-raboty")
    assert response.status_code == 404
    assert "detail" in response.json()


async def test_unpublished_hidden_from_public(client: AsyncClient) -> None:
    headers = await _auth_headers(client)
    created = await client.post(
        "/api/v1/admin/portfolio",
        json={
            "title": "Черновик",
            "slug": "chernovik",
            "is_published": False,
        },
        headers=headers,
    )
    assert created.status_code == 201
    assert (await client.get("/api/v1/portfolio/chernovik")).status_code == 404
    listed = await client.get("/api/v1/portfolio")
    assert listed.status_code == 200
    assert listed.json()["items"] == []
