"""Shared test fixtures."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator

import fakeredis.aioredis
import pytest
from httpx import ASGITransport, AsyncClient

# Ensure settings resolve before importing the app
os.environ.setdefault("API_BEARER_TOKEN", "test-token-123")
os.environ.setdefault("REDIS_URL", "")


@pytest.fixture()
def fake_redis():
    """Provide a fakeredis async client."""
    return fakeredis.aioredis.FakeRedis(decode_responses=True)


@pytest.fixture()
def app(fake_redis):
    """Create a fresh FastAPI app with Redis overridden to fakeredis."""
    # Import inside fixture so env vars are already set
    from app.main import create_app

    application = create_app()
    application.state.redis = fake_redis
    return application


@pytest.fixture()
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client wired to the ASGI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture()
def auth_headers() -> dict[str, str]:
    """Authorization headers with the test bearer token."""
    return {"Authorization": "Bearer test-token-123"}
