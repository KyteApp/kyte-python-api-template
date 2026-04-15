# Kyte Python Patterns -- Skill Index

Quick reference for common patterns used in Kyte Python API services.

## Contents

| Topic | File | Key Patterns |
|-------|------|-------------|
| FastAPI | [fastapi.md](fastapi.md) | App factory, routers, deps, lifespan, CORS, errors |
| Testing | [testing.md](testing.md) | conftest, fakeredis, AsyncClient, mocking, coverage |

## Quick Reference

### FastAPI Patterns
- **App factory**: `create_app()` in `app/main.py`
- **Routers**: Versioned under `app/api/v1/`
- **Dependencies**: `Depends()` for auth, Redis, services
- **Lifespan**: `@asynccontextmanager` for startup/shutdown
- **Error handling**: Custom exceptions + `add_exception_handler`
- **CORS**: `CORSMiddleware` with configurable origins
- **Background tasks**: `BackgroundTasks` parameter in handlers

### Pydantic v2 Patterns
- **BaseModel**: Request/response schemas in `app/models/`
- **Settings**: `BaseSettings` with env loading in `app/config.py`
- **Validators**: `@field_validator`, `@model_validator`
- **Serialization**: `model_dump()`, `model_validate()`
- **Generic models**: `PaginatedResponse[T]`

### Redis Patterns
- **Async client**: `redis.asyncio.from_url()`
- **Connection management**: via lifespan context manager
- **Pipelines**: `async with redis.pipeline() as pipe`
- **Key prefixing**: `f"{service}:{entity}:{id}"`
- **TTL**: Always set expiration on cache keys
- **Health check**: `await redis.ping()`

### Testing Patterns
- **conftest.py**: Shared fixtures for app, client, auth
- **fakeredis**: Drop-in async Redis replacement
- **AsyncClient**: Test endpoints via ASGI transport
- **Mocking**: `pytest-mock` for external services
- **Coverage**: `coverage run -m pytest`, minimum 50%

### Docker + CI/CD
- **Multi-stage builds**: Not needed for Python slim images
- **Non-root user**: `appuser` (uid 1000)
- **Healthcheck**: `curl /health`
- **CI**: Lint (ruff) + test (pytest) + coverage gate
- **CD**: Build + push to GHCR on main

### Security Patterns
- **Bearer token**: `verify_bearer_token` dependency
- **Input validation**: Pydantic models on all inputs
- **No secrets in code**: All via environment variables
- **CORS**: Restrict origins in production
- **Rate limiting**: Add via middleware for production
