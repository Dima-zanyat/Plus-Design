"""Тесты просмотра и обработки заявок администратором."""

import pytest
from httpx import AsyncClient

from app.config import settings

pytestmark = pytest.mark.asyncio


async def _auth_headers(client: AsyncClient) -> dict[str, str]:
    login = await client.post(
        "/api/v1/admin/login",
        json={"username": settings.admin_username, "password": settings.admin_password},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


async def test_list_leads_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/api/v1/admin/leads")
    assert response.status_code == 401


async def test_list_leads_returns_submitted_lead(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/leads",
        json={"name": "Анна Петрова", "phone": "+79991234567", "message": "Квартира 72м2"},
    )
    headers = await _auth_headers(client)
    response = await client.get("/api/v1/admin/leads", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["name"] == "Анна Петрова"
    assert body["items"][0]["status"] == "new"


async def test_update_lead_status(client: AsyncClient) -> None:
    created = await client.post(
        "/api/v1/leads",
        json={"name": "Иван Иванов", "phone": "+79997654321"},
    )
    lead_id = created.json()["id"]
    headers = await _auth_headers(client)

    response = await client.patch(
        f"/api/v1/admin/leads/{lead_id}",
        json={"status": "in_progress"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

    listed = await client.get("/api/v1/admin/leads", headers=headers)
    assert listed.json()["items"][0]["status"] == "in_progress"


async def test_update_missing_lead_status_returns_404(client: AsyncClient) -> None:
    headers = await _auth_headers(client)
    response = await client.patch(
        "/api/v1/admin/leads/999999",
        json={"status": "done"},
        headers=headers,
    )
    assert response.status_code == 404


async def test_update_lead_status_requires_auth(client: AsyncClient) -> None:
    created = await client.post(
        "/api/v1/leads",
        json={"name": "Пётр Петров", "phone": "+79995554433"},
    )
    lead_id = created.json()["id"]
    response = await client.patch(
        f"/api/v1/admin/leads/{lead_id}",
        json={"status": "done"},
    )
    assert response.status_code == 401
