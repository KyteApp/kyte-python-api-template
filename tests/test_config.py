"""Tests for configuration and models."""

from app.models.common import ErrorResponse, HealthResponse, PaginatedResponse


def test_redis_configured_true():
    """redis_configured should be True when redis_url is set."""
    from app.config import Settings
    s = Settings(redis_url="redis://localhost:6379/0")
    assert s.redis_configured is True


def test_redis_configured_false():
    """redis_configured should be False when redis_url is empty."""
    from app.config import Settings
    s = Settings(redis_url="")
    assert s.redis_configured is False


def test_paginated_response_total_pages():
    """PaginatedResponse.total_pages should compute correctly."""
    resp = PaginatedResponse(items=["a", "b"], total=10, page=1, page_size=3)
    assert resp.total_pages == 4  # ceil(10/3) = 4


def test_paginated_response_single_page():
    resp = PaginatedResponse(items=[], total=2, page=1, page_size=10)
    assert resp.total_pages == 1


def test_error_response():
    err = ErrorResponse(error="bad request", detail="field X missing")
    assert err.error == "bad request"
    assert err.detail == "field X missing"


def test_health_response_defaults():
    hr = HealthResponse(status="ok", service="test", version="1.0")
    assert hr.redis == "not_configured"
