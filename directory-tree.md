# Directory Tree (Single Source of Truth)

```
kyte-python-api-template/
├── app/
│   ├── __init__.py
│   ├── config.py                 # Pydantic Settings (env-driven config)
│   ├── main.py                   # App factory, lifespan, middleware
│   ├── api/
│   │   ├── __init__.py
│   │   ├── health.py             # /health, /ready endpoints
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── router.py         # V1 router aggregator
│   ├── core/
│   │   ├── __init__.py
│   │   ├── exceptions.py         # ServiceError, NotFoundError, handlers
│   │   └── security.py           # Bearer token dependency
│   ├── models/
│   │   ├── __init__.py
│   │   └── common.py             # HealthResponse, ErrorResponse, PaginatedResponse
│   ├── repositories/
│   │   └── __init__.py
│   └── services/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Shared fixtures (fakeredis, client, auth)
│   ├── test_health.py            # Health/ready/root endpoint tests
│   └── test_security.py          # Bearer auth tests
├── scripts/
│   └── .gitkeep
├── .claude/
│   ├── CLAUDE.md                 # Orchestrator config (modes, rules, agents)
│   ├── settings.json             # Claude Code permissions
│   ├── agents/
│   │   ├── subagent-python-architect.md
│   │   ├── subagent-qa-python.md
│   │   ├── subagent-security-analyst.md
│   │   └── subagent-docs-analyst.md
│   ├── commands/
│   │   ├── setup-project.md      # /setup-project slash command
│   │   └── create-subagent.md    # /create-subagent slash command
│   ├── hooks/
│   │   └── notify.sh             # Notification hook (macOS + Linux)
│   └── skills/
│       └── kyte-python-patterns/
│           ├── SKILL.md           # Pattern index
│           ├── fastapi.md         # FastAPI patterns
│           └── testing.md         # Testing patterns
├── .github/
│   └── workflows/
│       ├── ci.yml                # Lint + test + coverage
│       └── docker.yml            # Build + push to GHCR
├── CLAUDE.md                     # Project guide for Claude Code
├── README.md                     # Project documentation
├── directory-tree.md             # This file
├── pyproject.toml                # Project config, deps, tool settings
├── Dockerfile                    # Production container
├── docker-compose.yml            # Local development (Redis + API)
├── .env.example                  # Environment variable template
├── .gitignore
└── .dockerignore
```
