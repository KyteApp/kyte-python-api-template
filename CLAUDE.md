# CLAUDE.md -- Project Guide

> This file is the primary context for Claude Code when working on this project.
> Update it as the service evolves.

## Service: CHANGEME

**Stack:** Python 3.11 | FastAPI | Redis | httpx | Docker | ArgoCD

## Environments

| Env   | URL                          | Redis                  | Notes              |
|-------|------------------------------|------------------------|--------------------|
| LOCAL | http://localhost:8000        | redis://localhost:6379 | docker-compose     |
| STG   | https://CHANGEME.stg.kyte.cx | CHANGEME               | ArgoCD auto-deploy |
| PRD   | https://CHANGEME.kyte.cx     | CHANGEME               | Manual promotion   |

## Local Development

```bash
# 1. Create virtual environment
python -m venv venv && source venv/bin/activate

# 2. Install with dev dependencies
pip install -e ".[dev]"

# 3. Copy env
cp .env.example .env   # edit values as needed

# 4. Start Redis (or use docker-compose)
docker compose up redis -d

# 5. Run server
uvicorn app.main:app --reload --port 8000

# 6. Run tests
pytest -v

# 7. Lint
ruff check app/ tests/
```

## Key Commands

| Task           | Command                              |
|----------------|--------------------------------------|
| Run server     | `uvicorn app.main:app --reload`      |
| Run tests      | `pytest -v`                          |
| Coverage       | `coverage run -m pytest && coverage report` |
| Lint           | `ruff check app/ tests/`             |
| Format         | `ruff format app/ tests/`            |
| Docker build   | `docker compose build`               |
| Docker up      | `docker compose up`                  |

## Architecture

- **app/api/** -- Route handlers (health, v1/*)
- **app/core/** -- Security, exceptions, shared dependencies
- **app/models/** -- Pydantic models (request/response schemas)
- **app/services/** -- Business logic layer
- **app/repositories/** -- Data access layer (Redis, external APIs)
- **app/config.py** -- Pydantic Settings (env-driven)
- **app/main.py** -- App factory, lifespan, middleware

## Conventions

- All async -- use `async def` for handlers and services
- Bearer token auth via `verify_bearer_token` dependency
- Tests use fakeredis, never hit real Redis
- Coverage minimum: 50% (CI enforced)
- Ruff for linting (line-length 100)
