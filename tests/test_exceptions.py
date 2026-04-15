"""Tests for exception classes and handlers."""

import pytest
from fastapi import APIRouter

from app.core.exceptions import NotFoundError, ServiceError


def _register_error_routes(app):
    """Add routes that raise specific exceptions for testing."""
    router = APIRouter()

    @router.get("/raise-service-error")
    async def raise_service_error():
        raise ServiceError(message="something broke", status_code=500, detail="extra info")

    @router.get("/raise-service-error-no-detail")
    async def raise_service_error_no_detail():
        raise ServiceError(message="simple failure", status_code=422)

    @router.get("/raise-not-found")
    async def raise_not_found():
        raise NotFoundError(resource="Widget", identifier="abc-123")

    @router.get("/raise-not-found-no-id")
    async def raise_not_found_no_id():
        raise NotFoundError(resource="Widget")

    app.include_router(router)


@pytest.mark.asyncio
async def test_service_error_with_detail(app, client):
    _register_error_routes(app)
    resp = await client.get("/raise-service-error")
    assert resp.status_code == 500
    data = resp.json()
    assert data["error"] == "something broke"
    assert data["detail"] == "extra info"


@pytest.mark.asyncio
async def test_service_error_without_detail(app, client):
    _register_error_routes(app)
    resp = await client.get("/raise-service-error-no-detail")
    assert resp.status_code == 422
    data = resp.json()
    assert data["error"] == "simple failure"
    assert "detail" not in data


@pytest.mark.asyncio
async def test_not_found_with_identifier(app, client):
    _register_error_routes(app)
    resp = await client.get("/raise-not-found")
    assert resp.status_code == 404
    assert "Widget 'abc-123' not found" in resp.json()["error"]


@pytest.mark.asyncio
async def test_not_found_without_identifier(app, client):
    _register_error_routes(app)
    resp = await client.get("/raise-not-found-no-id")
    assert resp.status_code == 404
    assert resp.json()["error"] == "Widget not found"


def test_service_error_defaults():
    """ServiceError default values."""
    err = ServiceError()
    assert err.message == "Internal service error"
    assert err.status_code == 500
    assert err.detail is None


def test_not_found_is_service_error():
    """NotFoundError should be a subclass of ServiceError."""
    err = NotFoundError()
    assert isinstance(err, ServiceError)
    assert err.status_code == 404
