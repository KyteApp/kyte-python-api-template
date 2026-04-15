"""Tests for app lifespan (startup/shutdown) and security edge cases."""

import os
from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_lifespan_with_redis(fake_redis):
    """Lifespan should connect to Redis when configured."""
    os.environ["REDIS_URL"] = "redis://localhost:6379/0"

    # Reimport to pick up new env
    from app.config import Settings
    with patch("app.main.settings", Settings(redis_url="redis://fake:6379/0")):
        from app.main import create_app, lifespan
        app = create_app()

        # Mock Redis
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock()
        mock_redis.aclose = AsyncMock()

        with patch("app.main.aioredis") as mock_aioredis:
            mock_aioredis.from_url.return_value = mock_redis

            async with lifespan(app):
                # During lifespan, redis should be connected
                mock_redis.ping.assert_called_once()

            # After lifespan, redis should be closed
            mock_redis.aclose.assert_called_once()


@pytest.mark.asyncio
async def test_lifespan_without_redis():
    """Lifespan should work without Redis when not configured."""
    from app.config import Settings
    with patch("app.main.settings", Settings(redis_url="")):
        from app.main import create_app, lifespan
        app = create_app()

        async with lifespan(app):
            assert app.state.redis is None


@pytest.mark.asyncio
async def test_lifespan_redis_unreachable():
    """Lifespan should warn but continue if Redis is unreachable at startup."""
    from app.config import Settings
    with patch("app.main.settings", Settings(redis_url="redis://fake:6379/0")):
        from app.main import create_app, lifespan
        app = create_app()

        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock(side_effect=ConnectionError("refused"))
        mock_redis.aclose = AsyncMock()

        with patch("app.main.aioredis") as mock_aioredis:
            mock_aioredis.from_url.return_value = mock_redis

            async with lifespan(app):
                # Should not crash, just warn
                pass

            mock_redis.aclose.assert_called_once()


@pytest.mark.asyncio
async def test_bearer_token_not_configured(app, client):
    """When API_BEARER_TOKEN is empty, protected route should return 500."""
    from fastapi import APIRouter, Depends

    from app.core.security import verify_bearer_token

    router = APIRouter()

    @router.get("/test-no-token")
    async def route(token: str = Depends(verify_bearer_token)):
        return {"ok": True}

    app.include_router(router)

    with patch("app.core.security.settings") as mock_settings:
        mock_settings.api_bearer_token = ""
        resp = await client.get("/test-no-token", headers={"Authorization": "Bearer anything"})
        assert resp.status_code == 500
        assert "not configured" in resp.json()["detail"]
