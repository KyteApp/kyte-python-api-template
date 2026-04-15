# FastAPI Patterns

Detailed reference for FastAPI patterns used at Kyte.

## App Factory Pattern

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to databases, initialize clients
    app.state.redis = await create_redis_pool()
    yield
    # Shutdown: close connections, cleanup
    await app.state.redis.aclose()

def create_app() -> FastAPI:
    app = FastAPI(
        title="My Service",
        version="1.0.0",
        lifespan=lifespan,
    )
    # Add middleware
    # Add exception handlers
    # Include routers
    return app

app = create_app()
```

## Router Organization

```
app/api/
    health.py          # /health, /ready (no prefix, no auth)
    v1/
        router.py      # APIRouter(prefix="/v1") -- aggregates sub-routers
        items.py       # APIRouter() -- registered in router.py with prefix="/items"
        orders.py      # APIRouter() -- registered in router.py with prefix="/orders"
```

### Creating a New Router

```python
# app/api/v1/items.py
from fastapi import APIRouter, Depends
from app.core.security import verify_bearer_token
from app.models.items import ItemResponse, CreateItemRequest

router = APIRouter()

@router.get("/", response_model=list[ItemResponse])
async def list_items():
    ...

@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(body: CreateItemRequest):
    ...

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    ...
```

### Registering in v1 Router

```python
# app/api/v1/router.py
from fastapi import APIRouter, Depends
from app.core.security import verify_bearer_token
from app.api.v1 import items

router = APIRouter(prefix="/v1")
router.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(verify_bearer_token)],
)
```

## Dependency Injection

### Getting Redis from App State

```python
from fastapi import Request

async def get_redis(request: Request):
    return request.app.state.redis

# Usage in handler:
@router.get("/data")
async def get_data(redis = Depends(get_redis)):
    value = await redis.get("key")
    ...
```

### Service Dependencies

```python
from app.services.item_service import ItemService
from app.repositories.item_repo import ItemRepository

async def get_item_service(request: Request) -> ItemService:
    redis = request.app.state.redis
    repo = ItemRepository(redis)
    return ItemService(repo)

@router.get("/items")
async def list_items(service: ItemService = Depends(get_item_service)):
    return await service.list_all()
```

## Lifespan Context Manager

The lifespan replaces the deprecated `on_startup` / `on_shutdown` events.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    logging.basicConfig(level=settings.log_level)

    # Connect Redis
    if settings.redis_configured:
        app.state.redis = aioredis.from_url(settings.redis_url)
        await app.state.redis.ping()
    else:
        app.state.redis = None

    # Initialize HTTP client pool
    app.state.http_client = httpx.AsyncClient(timeout=30)

    logger.info("Service started")

    yield  # App is running

    # SHUTDOWN
    await app.state.http_client.aclose()
    if app.state.redis:
        await app.state.redis.aclose()
    logger.info("Service stopped")
```

## Error Handling

### Custom Exceptions

```python
class ServiceError(Exception):
    def __init__(self, message, status_code=500, detail=None):
        self.message = message
        self.status_code = status_code
        self.detail = detail

class NotFoundError(ServiceError):
    def __init__(self, resource, identifier=None):
        msg = f"{resource} '{identifier}' not found"
        super().__init__(msg, status_code=404)

class ValidationError(ServiceError):
    def __init__(self, message, detail=None):
        super().__init__(message, status_code=422, detail=detail)
```

### Exception Handlers

```python
async def generic_error_handler(request, exc: ServiceError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "detail": exc.detail},
    )

app.add_exception_handler(ServiceError, generic_error_handler)
```

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

# Development: allow all
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Production: restrict
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.kyte.com"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## Background Tasks

```python
from fastapi import BackgroundTasks

async def send_notification(user_id: str, message: str):
    # Long-running task
    ...

@router.post("/orders")
async def create_order(body: CreateOrderRequest, bg: BackgroundTasks):
    order = await service.create(body)
    bg.add_task(send_notification, order.user_id, "Order created!")
    return order
```
