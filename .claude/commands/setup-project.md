---
name: setup-project
description: Initialize a new project from the Kyte Python API template
---

# /setup-project

Initialize a new Python API service from this template.

## Steps

1. **Ask for the service name** (e.g., `order-service`, `notification-service`)
2. **Rename the package**:
   - Update `name` in `pyproject.toml` to the new service name
   - Update `service_name` default in `app/config.py`
   - Update `IMAGE_NAME` in `.github/workflows/docker.yml` (replace CHANGEME)
   - Update service references in `CLAUDE.md`
   - Update `docker-compose.yml` service name if desired
3. **Create .env from .env.example**:
   ```bash
   cp .env.example .env
   ```
   Update `SERVICE_NAME` in the new `.env`
4. **Install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e ".[dev]"
   ```
5. **Run tests to verify**:
   ```bash
   pytest -v
   ```
6. **Run linter**:
   ```bash
   ruff check app/ tests/
   ```
7. **Report results** -- confirm all tests pass and lint is clean

## Checklist

- [ ] pyproject.toml name updated
- [ ] app/config.py SERVICE_NAME updated
- [ ] docker.yml IMAGE_NAME updated
- [ ] CLAUDE.md service references updated
- [ ] .env created from .env.example
- [ ] pip install succeeded
- [ ] All tests pass
- [ ] Lint clean
