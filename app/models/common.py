"""Shared response models used across the API."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class HealthResponse(BaseModel):
    """Response for health / readiness probes."""

    status: str = Field(examples=["ok"])
    service: str
    version: str
    redis: str = Field(default="not_configured", examples=["connected", "disconnected", "not_configured"])


class ErrorResponse(BaseModel):
    """Standard error envelope."""

    error: str = Field(description="Human-readable error message")
    detail: str | None = Field(default=None, description="Optional extra detail")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""

    items: list[T]
    total: int = Field(ge=0, description="Total items available")
    page: int = Field(ge=1, description="Current page (1-based)")
    page_size: int = Field(ge=1, description="Items per page")

    @property
    def total_pages(self) -> int:
        return max(1, -(-self.total // self.page_size))  # ceiling division
