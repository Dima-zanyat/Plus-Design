"""Тесты формы-заявки."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_minimal_lead_without_email(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/leads", json={"name": "Дмитрий", "phone": "+7 999 123-45-67"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] is None
    assert body["status"] == "new"
    assert body["phone"] == "+79991234567"


async def test_lead_with_email_and_message(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/leads",
        json={
            "name": "Анна Петрова",
            "phone": "89991234567",
            "email": "anna@example.com",
            "message": "Нужен лендинг",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "anna@example.com"
    assert body["phone"] == "+79991234567"


async def test_phone_is_required(client: AsyncClient) -> None:
    response = await client.post("/api/v1/leads", json={"name": "Дмитрий"})
    assert response.status_code == 422


@pytest.mark.parametrize("phone", ["123", "не телефон", "+7(999)abc-45-67", ""])
async def test_invalid_phone_rejected(client: AsyncClient, phone: str) -> None:
    response = await client.post(
        "/api/v1/leads", json={"name": "Дмитрий", "phone": phone}
    )
    assert response.status_code == 422


async def test_invalid_email_rejected(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/leads",
        json={"name": "Дмитрий", "phone": "+79991234567", "email": "не-почта"},
    )
    assert response.status_code == 422


async def test_short_name_rejected(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/leads", json={"name": "Д", "phone": "+79991234567"}
    )
    assert response.status_code == 422


async def test_duplicate_submission_conflicts(client: AsyncClient) -> None:
    payload = {"name": "Дмитрий", "phone": "+79991234567"}
    assert (await client.post("/api/v1/leads", json=payload)).status_code == 201
    repeat = await client.post("/api/v1/leads", json=payload)
    assert repeat.status_code == 409
