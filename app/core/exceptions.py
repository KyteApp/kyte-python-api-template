"""Custom exception hierarchy and FastAPI exception handlers."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class ServiceError(Exception):
    """Base exception for all domain / service errors."""

    def __init__(self, message: str = "Internal service error", status_code: int = 500, detail: Any = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.detail = detail


class NotFoundError(ServiceError):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str = "Resource", identifier: str | None = None):
        msg = f"{resource} not found" if not identifier else f"{resource} '{identifier}' not found"
        super().__init__(message=msg, status_code=404)


# ---------------------------------------------------------------------------
# FastAPI exception handlers
# ---------------------------------------------------------------------------

async def generic_error_handler(request: Request, exc: ServiceError) -> JSONResponse:
    """Handle all ServiceError subclasses."""
    logger.error("ServiceError: %s (status=%d)", exc.message, exc.status_code)
    body: dict[str, Any] = {"error": exc.message}
    if exc.detail is not None:
        body["detail"] = exc.detail
    return JSONResponse(status_code=exc.status_code, content=body)


async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    """Handle NotFoundError specifically (also caught by generic, but allows customization)."""
    return JSONResponse(status_code=404, content={"error": exc.message})
