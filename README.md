# Kyte Python API Template

Production-ready template for building Python API services at Kyte. Built on FastAPI + Redis + httpx with full Docker, CI/CD, and Claude Code integration.

## What This Template Provides

- **FastAPI** application with app factory pattern and async lifespan management
- **Redis** integration with async client and health checks
- **Pydantic v2** for configuration (Settings) and request/response models
- **Bearer token authentication** middleware
- **Health and readiness** endpoints for Kubernetes probes
- **Versioned API** router structure (`/v1/...`)
- **Test suite** with pytest, fakeredis, and AsyncClient
- **Docker** and docker-compose for local development
- **GitHub Actions** CI/CD (lint, test, coverage, Docker build)
- **Claude Code** agents, skills, commands, and hooks

## Quick Start

### 1. Use This Template

Click "Use this template" on GitHub, or clone directly:

```bash
git clone https://github.com/KyteApp/kyte-python-api-template.git my-service
cd my-service
```

### 2. Set Up Your Project

If using Claude Code, run the setup command:

```
/setup-project
```

Or manually:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"

# Create .env from example
cp .env.example .env
# Edit .env with your values
```

### 3. Run Tests

```bash
pytest -v
```

### 4. Start the Server

```bash
# Option A: Without Redis
uvicorn app.main:app --reload --port 8000

# Option B: With Redis (via Docker)
docker compose up redis -d
uvicorn app.main:app --reload --port 8000

# Option C: Full stack via Docker
docker compose up
```

### 5. Explore

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Readiness: http://localhost:8000/ready

## Architecture

```
Request -> FastAPI -> Router -> Handler -> Service -> Repository -> Redis/External
                       |
                  Middleware (CORS, Auth)
```

### Layers

| Layer | Directory | Responsibility |
|-------|-----------|----------------|
| **API** | `app/api/` | HTTP handlers, request/response mapping |
| **Core** | `app/core/` | Cross-cutting: auth, exceptions, shared deps |
| **Models** | `app/models/` | Pydantic schemas (request, response, domain) |
| **Services** | `app/services/` | Business logic, orchestration |
| **Repositories** | `app/repositories/` | Data access (Redis, external APIs via httpx) |
| **Config** | `app/config.py` | Environment-driven settings |

### Directory Structure

See [directory-tree.md](directory-tree.md) for the complete file tree.

## How to Add New Endpoints

### 1. Create the Model

```python
# app/models/items.py
from pydantic import BaseModel, Field

class ItemResponse(BaseModel):
    id: str
    name: str
    price: float

class CreateItemRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
```

### 2. Create the Repository (optional)

```python
# app/repositories/item_repo.py
import json
from redis.asyncio import Redis

class ItemRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, item_id: str) -> dict | None:
        data = await self.redis.get(f"item:{item_id}")
        return json.loads(data) if data else None

    async def save(self, item_id: str, data: dict) -> None:
        await self.redis.set(f"item:{item_id}", json.dumps(data), ex=3600)
```

### 3. Create the Service

```python
# app/services/item_service.py
from app.repositories.item_repo import ItemRepository
from app.core.exceptions import NotFoundError

class ItemService:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def get_item(self, item_id: str) -> dict:
        item = await self.repo.get(item_id)
        if not item:
            raise NotFoundError("Item", item_id)
        return item
```

### 4. Create the Router

```python
# app/api/v1/items.py
from fastapi import APIRouter, Depends, Request
from app.models.items import ItemResponse
from app.services.item_service import ItemService
from app.repositories.item_repo import ItemRepository

router = APIRouter()

async def get_service(request: Request) -> ItemService:
    repo = ItemRepository(request.app.state.redis)
    return ItemService(repo)

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str, service: ItemService = Depends(get_service)):
    return await service.get_item(item_id)
```

### 5. Register in v1 Router

```python
# app/api/v1/router.py
from fastapi import Depends
from app.core.security import verify_bearer_token
from app.api.v1 import items

router.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(verify_bearer_token)],
)
```

### 6. Write Tests

```python
# tests/test_v1_items.py
import pytest

@pytest.mark.asyncio
async def test_get_item(client, auth_headers, fake_redis):
    await fake_redis.set("item:123", '{"id":"123","name":"Widget","price":9.99}')
    resp = await client.get("/v1/items/123", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Widget"

@pytest.mark.asyncio
async def test_get_item_not_found(client, auth_headers):
    resp = await client.get("/v1/items/999", headers=auth_headers)
    assert resp.status_code == 404
```

## Testing Guide

### Run Tests

```bash
# All tests
pytest -v

# Specific file
pytest tests/test_health.py -v

# With coverage
coverage run -m pytest
coverage report
coverage html  # Open htmlcov/index.html
```

### Test Stack

| Tool | Purpose |
|------|---------|
| pytest | Test framework |
| pytest-asyncio | Async test support |
| fakeredis | In-memory Redis replacement |
| httpx AsyncClient | ASGI test client |
| pytest-mock | Mocking utilities |
| coverage | Code coverage measurement |

### Writing Tests

- Put shared fixtures in `tests/conftest.py`
- Use `fakeredis` -- never connect to real Redis in tests
- Use `AsyncClient` with `ASGITransport` for endpoint tests
- Mock external HTTP calls with `pytest-mock`
- Coverage minimum: 50% (enforced in CI)

## Docker and Deployment

### Local Development

```bash
docker compose up        # Full stack (Redis + API)
docker compose up redis  # Just Redis
```

### Production Build

```bash
docker build -t my-service .
docker run -p 8000:8000 --env-file .env my-service
```

### CI/CD

| Workflow | Trigger | Actions |
|----------|---------|---------|
| `ci.yml` | Push to main/develop, PRs | Lint (ruff), test (pytest), coverage check |
| `docker.yml` | Push to main | Build and push to GHCR |

### Customizing for Your Service

Update the `IMAGE_NAME` in `.github/workflows/docker.yml`:

```yaml
IMAGE_NAME: your-org/your-service-name
```

## Claude Code Integration

This template includes full Claude Code support for AI-assisted development.

### Agents

| Agent | Purpose |
|-------|---------|
| python-architect | API design, models, architecture decisions |
| qa-python | Test plans, test code, coverage improvement |
| security-analyst | OWASP review, auth audit, dependency check |
| docs-analyst | README, CLAUDE.md, API documentation |

### Skills

The `kyte-python-patterns` skill provides quick-reference documentation for:
- FastAPI patterns (app factory, routers, dependencies, lifespan)
- Testing patterns (conftest, fakeredis, AsyncClient, mocking)

### Commands

| Command | Description |
|---------|-------------|
| `/setup-project` | Initialize from template (rename, configure, install, test) |
| `/create-subagent` | Interactive wizard to create new Claude Code agents |

## Configuration

All configuration is via environment variables. See [.env.example](.env.example) for the full list.

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVICE_NAME` | kyte-python-api-template | Display name |
| `SERVICE_VERSION` | 0.1.0 | Semantic version |
| `HOST` | 0.0.0.0 | Bind host |
| `PORT` | 8000 | Bind port |
| `WORKERS` | 1 | Uvicorn workers |
| `INSTANCE_ID` | local | Pod/instance ID |
| `PUBLIC_URL` | http://localhost:8000 | External URL |
| `REDIS_URL` | (empty) | Redis connection string |
| `API_BEARER_TOKEN` | (empty) | Bearer token for auth |
| `LOG_LEVEL` | INFO | Python log level |

## Contributing

1. Create a feature branch from `develop`
2. Write tests first (TDD)
3. Implement the feature
4. Ensure `pytest` passes and `ruff check` is clean
5. Open a PR to `develop`
