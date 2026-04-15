"""Tests for health, readiness, and root endpoints."""

from unittest.mock import AsyncMock

import pytest


@pytest.mark.asyncio
async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "service" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_ready(client):
    resp = await client.get("/ready")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["redis"] == "connected"


@pytest.mark.asyncio
async def test_ready_redis_disconnected(app, client):
    """Readiness should report disconnected when Redis ping fails."""
    failing_redis = AsyncMock()
    failing_redis.ping.side_effect = ConnectionError("redis down")
    app.state.redis = failing_redis

    resp = await client.get("/ready")
    assert resp.status_code == 200
    assert resp.json()["redis"] == "disconnected"


@pytest.mark.asyncio
async def test_ready_redis_not_configured(app, client):
    """Readiness should report not_configured when Redis is None."""
    app.state.redis = None

    resp = await client.get("/ready")
    assert resp.status_code == 200
    assert resp.json()["redis"] == "not_configured"


@pytest.mark.asyncio
async def test_root(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "service" in data
    assert "version" in data
    assert "docs" in data
