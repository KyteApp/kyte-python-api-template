"""FastAPI application factory and lifespan management."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.v1.router import router as v1_router
from app.config import settings
from app.core.exceptions import (
    NotFoundError,
    ServiceError,
    generic_error_handler,
    not_found_handler,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage startup / shutdown resources."""
    logging.basicConfig(level=settings.log_level.upper(), format="%(asctime)s %(levelname)s %(name)s — %(message)s")

    # --- Startup ---
    if settings.redis_configured:
        app.state.redis = aioredis.from_url(
            settings.redis_url,
            decode_responses=True,
            socket_connect_timeout=5,
        )
        try:
            await app.state.redis.ping()
            logger.info("Redis connected: %s", settings.redis_url)
        except Exception:
            logger.warning("Redis not reachable at startup — will retry on demand")
    else:
        app.state.redis = None
        logger.info("Redis not configured — running without cache")

    logger.info(
        "Service %s v%s started (instance=%s)",
        settings.service_name,
        settings.service_version,
        settings.instance_id,
    )

    yield

    # --- Shutdown ---
    if app.state.redis is not None:
        await app.state.redis.aclose()
        logger.info("Redis connection closed")

    logger.info("Service shutdown complete")


def create_app() -> FastAPI:
    """Build and return the configured FastAPI application."""
    app = FastAPI(
        title=settings.service_name,
        version=settings.service_version,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # -- CORS --
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -- Exception handlers --
    app.add_exception_handler(ServiceError, generic_error_handler)
    app.add_exception_handler(NotFoundError, not_found_handler)

    # -- Routers --
    app.include_router(health_router)
    app.include_router(v1_router)

    # -- Root --
    @app.get("/", tags=["root"])
    async def root(request: Request) -> dict:
        return {
            "service": settings.service_name,
            "version": settings.service_version,
            "docs": str(request.url_for("swagger_ui_html")),
        }

    return app


app = create_app()
