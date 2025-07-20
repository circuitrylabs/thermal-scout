# Local API Development Guide

This guide covers setting up and developing the Thermal Scout API locally.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Git

## Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd thermal-scout

# Install dependencies with uv
uv sync --extra dev

# Run the API server
uv run python run_api.py
```

The API will be available at:
- API Base: http://localhost:8080
- Interactive Docs: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## Project Structure

```
thermal-scout/
├── thermal_scout/
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py          # FastAPI application
│   ├── search.py            # Core search functionality
│   └── cli.py               # CLI interface
├── tests/
│   ├── test_api.py          # API tests
│   └── test_search.py       # Search tests
├── docs/
│   ├── API.md               # API reference
│   └── LOCAL_DEVELOPMENT.md # This file
├── run_api.py               # API runner script
└── pyproject.toml           # Project configuration
```

## Development Workflow

### 1. Environment Setup

```bash
# Create and activate virtual environment (handled by uv)
uv sync --extra dev

# Verify installation
uv run python -c "import thermal_scout; print('✅ Setup complete')"
```

### 2. Running the API

#### Development Mode (with auto-reload)

```bash
uv run python run_api.py
# or
uv run uvicorn thermal_scout.api.main:app --reload --port 8080
```

#### Production Mode

```bash
uv run uvicorn thermal_scout.api.main:app --host 0.0.0.0 --port 8080
```

#### Custom Configuration

```bash
# Change port
uv run uvicorn thermal_scout.api.main:app --port 8000

# Enable debug logging
uv run uvicorn thermal_scout.api.main:app --log-level debug

# Bind to specific interface
uv run uvicorn thermal_scout.api.main:app --host 127.0.0.1
```

### 3. Testing

#### Run All Tests

```bash
uv run pytest
```

#### Run Specific Tests

```bash
# Test only API endpoints
uv run pytest tests/test_api.py

# Test with coverage
uv run pytest --cov=thermal_scout

# Run specific test
uv run pytest tests/test_api.py::TestSearchEndpoint::test_search_returns_model_list
```

#### Test in Watch Mode

```bash
# Install pytest-watch if needed
uv add --dev pytest-watch

# Run tests in watch mode
uv run ptw
```

### 4. Code Quality

#### Linting with Ruff

```bash
# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

#### Type Checking

```bash
# Run mypy
uv run mypy thermal_scout/
```

#### Pre-commit Hooks

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

## API Development Tips

### Adding New Endpoints

1. **Define Pydantic Models** in `api/main.py`:

```python
class NewFeatureRequest(BaseModel):
    field1: str
    field2: int = 10
    
class NewFeatureResponse(BaseModel):
    result: str
    metadata: dict[str, Any]
```

2. **Create Endpoint**:

```python
@app.post("/api/v1/new-feature", response_model=NewFeatureResponse)
async def new_feature(request: NewFeatureRequest):
    """
    Document your endpoint here
    """
    # Implementation
    return NewFeatureResponse(...)
```

3. **Add Tests**:

```python
def test_new_feature(client):
    response = client.post("/api/v1/new-feature", json={
        "field1": "test",
        "field2": 20
    })
    assert response.status_code == 200
    assert response.json()["result"] == "expected"
```

### Error Handling

Use FastAPI's HTTPException for consistent error responses:

```python
from fastapi import HTTPException

if not model_found:
    raise HTTPException(
        status_code=404,
        detail=f"Model {model_id} not found"
    )
```

### Adding Dependencies

```bash
# Add runtime dependency
uv add package-name

# Add dev dependency
uv add --dev package-name
```

## Debugging

### Enable Debug Mode

```python
# In run_api.py or when running uvicorn
uvicorn.run(app, host="0.0.0.0", port=8080, reload=True, log_level="debug")
```

### Using Python Debugger

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use the built-in breakpoint()
breakpoint()
```

### VS Code Debugging

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug API",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "thermal_scout.api.main:app",
        "--reload",
        "--port", "8080"
      ],
      "jinja": true,
      "justMyCode": true
    }
  ]
}
```

## Common Issues

### Port Already in Use

```bash
# Find process using port 8080
lsof -i :8080

# Kill the process
kill -9 <PID>
```

### Module Import Errors

```bash
# Ensure you're in the project root
cd /path/to/thermal-scout

# Reinstall in development mode
uv pip install -e .
```

### CORS Issues

Check that your frontend URL is in the CORS allowed origins:

```python
# In api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://your-frontend:3000"],
    # ...
)
```

## Performance Optimization

### Caching

Add caching for expensive operations:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_operation(param: str):
    # Cached computation
    pass
```

### Async Operations

Use async/await for I/O operations:

```python
import httpx

async def fetch_external_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

## Deployment Preparation

### Environment Variables

Create `.env` file for configuration:

```bash
# .env
API_HOST=0.0.0.0
API_PORT=8080
LOG_LEVEL=info
CORS_ORIGINS=["https://production.com"]
```

Load in your app:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_host: str = "0.0.0.0"
    api_port: int = 8080
    log_level: str = "info"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Docker Support

Create `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy files
COPY pyproject.toml uv.lock ./
COPY thermal_scout/ ./thermal_scout/

# Install dependencies
RUN uv sync --frozen --no-dev

# Run API
CMD ["uv", "run", "uvicorn", "thermal_scout.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## Next Steps

1. Set up continuous integration (GitHub Actions)
2. Add authentication/authorization
3. Implement rate limiting
4. Add monitoring/observability
5. Create client SDKs
6. Set up API versioning strategy

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [uv Documentation](https://github.com/astral-sh/uv)