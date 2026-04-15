"""Tests for bearer token authentication."""

import pytest
from fastapi import APIRouter, Depends

from app.core.security import verify_bearer_token


def _register_protected_route(app):
    """Add a temporary protected route for testing."""
    test_router = APIRouter()

    @test_router.get("/test-protected")
    async def protected(token: str = Depends(verify_bearer_token)):
        return {"message": "access granted", "token": token}

    app.include_router(test_router)


@pytest.mark.asyncio
async def test_bearer_required(app, client):
    """Request without Authorization header should return 401."""
    _register_protected_route(app)
    resp = await client.get("/test-protected")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_bearer_valid(app, client, auth_headers):
    """Valid bearer token should pass."""
    _register_protected_route(app)
    resp = await client.get("/test-protected", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "access granted"


@pytest.mark.asyncio
async def test_bearer_invalid(app, client):
    """Wrong bearer token should return 403."""
    _register_protected_route(app)
    resp = await client.get("/test-protected", headers={"Authorization": "Bearer wrong-token"})
    assert resp.status_code == 403
