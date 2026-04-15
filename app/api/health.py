"""Health and readiness endpoints.

These are intentionally unauthenticated so that load balancers, Kubernetes
probes, and monitoring tools can reach them.
"""

import logging

from fastapi import APIRouter, Request

from app.config import settings
from app.models.common import HealthResponse

router = APIRouter(tags=["health"])
logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    """Liveness probe -- always returns 200 if the process is running."""
    return HealthResponse(
        status="ok",
        service=settings.service_name,
        version=settings.service_version,
    )


@router.get("/ready", response_model=HealthResponse)
async def ready(request: Request) -> HealthResponse:
    """Readiness probe -- checks dependent services (Redis)."""
    redis_status = "not_configured"
    redis_client = getattr(request.app.state, "redis", None)

    if redis_client is not None:
        try:
            await redis_client.ping()
            redis_status = "connected"
        except Exception:
            logger.warning("Redis readiness check failed")
            redis_status = "disconnected"

    return HealthResponse(
        status="ok",
        service=settings.service_name,
        version=settings.service_version,
        redis=redis_status,
    )
