# Testing Patterns

Detailed reference for testing patterns in Kyte Python API services.

## conftest.py Structure

```python
import os
import fakeredis.aioredis
import pytest
from httpx import ASGITransport, AsyncClient

# Set test environment BEFORE importing app
os.environ["API_BEARER_TOKEN"] = "test-token"
os.environ["REDIS_URL"] = ""

@pytest.fixture()
def fake_redis():
    return fakeredis.aioredis.FakeRedis(decode_responses=True)

@pytest.fixture()
def app(fake_redis):
    from app.main import create_app
    application = create_app()
    application.state.redis = fake_redis
    return application

@pytest.fixture()
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture()
def auth_headers():
    return {"Authorization": "Bearer test-token"}
```

## fakeredis Fixtures

### Basic Usage

```python
@pytest.fixture()
def fake_redis():
    return fakeredis.aioredis.FakeRedis(decode_responses=True)
```

### Pre-populated Redis

```python
@pytest.fixture()
async def redis_with_data(fake_redis):
    await fake_redis.set("user:123", '{"name": "John"}')
    await fake_redis.set("user:456", '{"name": "Jane"}')
    return fake_redis
```

### Shared Server (when tests need to share state)

```python
@pytest.fixture()
def redis_server():
    server = fakeredis.FakeServer()
    return server

@pytest.fixture()
def fake_redis(redis_server):
    return fakeredis.aioredis.FakeRedis(server=redis_server, decode_responses=True)
```

## AsyncClient Usage

### Basic Request

```python
async def test_list_items(client, auth_headers):
    resp = await client.get("/v1/items", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
```

### POST with JSON Body

```python
async def test_create_item(client, auth_headers):
    payload = {"name": "Widget", "price": 9.99}
    resp = await client.post("/v1/items", json=payload, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Widget"
```

### Query Parameters

```python
async def test_search(client, auth_headers):
    resp = await client.get("/v1/items", params={"q": "widget", "page": 1}, headers=auth_headers)
    assert resp.status_code == 200
```

### File Upload

```python
async def test_upload(client, auth_headers):
    files = {"file": ("test.csv", b"col1,col2\n1,2", "text/csv")}
    resp = await client.post("/v1/upload", files=files, headers=auth_headers)
    assert resp.status_code == 200
```

## Mocking External Services

### Using pytest-mock

```python
async def test_external_call(client, auth_headers, mocker):
    mock_response = mocker.AsyncMock(return_value={"result": "ok"})
    mocker.patch("app.services.external.fetch_data", mock_response)

    resp = await client.get("/v1/data", headers=auth_headers)
    assert resp.status_code == 200
    mock_response.assert_called_once()
```

### Mocking httpx Client

```python
import httpx

async def test_with_mocked_http(client, auth_headers, mocker):
    mock_resp = httpx.Response(200, json={"status": "ok"})
    mocker.patch("httpx.AsyncClient.get", return_value=mock_resp)

    resp = await client.get("/v1/proxy-data", headers=auth_headers)
    assert resp.status_code == 200
```

## Coverage Configuration

### pyproject.toml

```toml
[tool.coverage.run]
source = ["app"]
omit = ["app/__init__.py"]

[tool.coverage.report]
fail_under = 50
show_missing = true
```

### Running Coverage

```bash
# Run with coverage
coverage run -m pytest

# Show report
coverage report

# Generate HTML report
coverage html
# Open htmlcov/index.html

# Generate XML (for CI)
coverage xml
```

## Test Organization

```
tests/
    __init__.py
    conftest.py              # Shared fixtures
    test_health.py           # Health/ready endpoints
    test_security.py         # Auth tests
    test_v1_items.py         # V1 items endpoint tests
    test_v1_orders.py        # V1 orders endpoint tests
    test_item_service.py     # Unit tests for service layer
    test_item_repo.py        # Unit tests for repository layer
```

## Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("status_code,token", [
    (403, None),           # No token
    (403, "wrong"),        # Wrong token
    (200, "test-token"),   # Correct token
])
async def test_auth_scenarios(client, status_code, token):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = await client.get("/v1/protected", headers=headers)
    assert resp.status_code == status_code
```
