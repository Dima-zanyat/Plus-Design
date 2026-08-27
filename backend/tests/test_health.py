"""Тесты healthcheck."""

import pytest

from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_health_ok(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_health_db_ok(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health/db")
    assert response.status_code == 200
    assert response.json()["database"] == "ok"
