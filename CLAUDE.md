# CLAUDE.md - Thermal Scout

Project guidance for Claude Code when developing Thermal Scout.

## Project Overview

Thermal Scout is a minimal AI model search tool with thermal cost awareness. It provides three interfaces:

1. **Web UI** - Clean, light-mode interface (vanilla HTML/CSS/JS)
2. **CLI** - Command-line tool built with Typer
3. **API** - REST API built with FastAPI

## Quick Commands

```bash
# Development
uv sync                    # Install dependencies
uv run pytest             # Run tests
uv run ruff format .      # Format code
uv run ruff check .       # Lint
uv run ty                 # Type check

# Run services
python -m http.server 8000              # Web UI
uv run python -m thermal_scout.cli      # CLI
uv run python run_api.py                # API server
```

## Architecture

### Stack
- **Python 3.12+** with type hints
- **uv** - Package management
- **ruff** - Linting/formatting
- **ty** - Type checking
- **Typer** - CLI framework
- **FastAPI** - API framework
- **Vanilla HTML/CSS/JS** - No build tools

### Project Structure
```
thermal-scout/
├── index.html              # Single-page web app
├── app.js                 # Frontend logic
├── styles.css             # Light-mode only styling
├── thermal_scout/         # Python package
│   ├── __init__.py       # Package exports
│   ├── cli.py           # Typer CLI
│   ├── search.py        # Core search logic
│   └── api/             # FastAPI app
│       ├── __init__.py
│       └── main.py      # API endpoints
├── tests/               # Test suite
│   ├── conftest.py     # Test fixtures
│   ├── test_search.py  # Core tests
│   ├── test_cli.py     # CLI tests
│   └── test_api.py     # API tests
├── pyproject.toml      # Project config
└── docs/              # Documentation
```

## Development Guidelines

### Python Code Style

```python
# Use type hints everywhere
def search_models(query: str, limit: int = 20) -> list[dict[str, Any]]:
    """Search HuggingFace models with thermal awareness."""
    ...

# Keep functions focused and testable
def get_thermal_indicator(parameters: int) -> str:
    if parameters < 1e9:
        return "Cool"
    ...
```

### Frontend Guidelines

```javascript
// Module pattern for organization
const ThermalScout = (() => {
    const state = {
        models: []
    };
    
    function init() {
        // Initialize app
    }
    
    return { init };
})();

// No external dependencies
// Light mode only - no dark theme
```

### API Design

```python
# FastAPI with clear types
@app.get("/api/v1/search")
async def search(
    q: str,
    limit: int = 20,
    thermal: str | None = None
) -> SearchResponse:
    """Search models with optional thermal filtering."""
    ...
```

## Thermal Cost Algorithm

Models are categorized by parameter count:

- **Cool** 🟢: <1B parameters
- **Warm** 🟡: 1-3B parameters  
- **Moderate** 🟠: 3-7B parameters
- **Hot** 🔴: 7B+ parameters

## Testing

```bash
# Run all tests
uv run pytest

# Run specific test
uv run pytest tests/test_search.py::test_thermal_indicator

# With coverage
uv run pytest --cov=thermal_scout --cov-report=html
```

## Common Tasks

### Add a New Feature

1. Write tests first in `tests/`
2. Implement in appropriate module
3. Update documentation
4. Run full test suite
5. Format and lint code

### Update Dependencies

```bash
# Add a dependency
uv add package-name

# Add dev dependency
uv add --dev package-name

# Update all
uv sync
```

### Debug Issues

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check API responses
curl http://localhost:8080/api/v1/search?q=llama
```

## Important Notes

1. **No API keys required** - Direct HuggingFace Hub access
2. **Light mode only** - No dark theme support
3. **Minimal dependencies** - Keep it simple
4. **Type safety** - Use type hints everywhere
5. **Test coverage** - Maintain >95% coverage

## Code Patterns to Follow

### Error Handling
```python
try:
    result = search_models(query)
except Exception as e:
    logger.error(f"Search failed: {e}")
    raise HTTPException(status_code=500, detail="Search failed")
```

### Async Operations
```python
async def fetch_models(query: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(...)
        return response.json()
```

### CLI Commands
```python
@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(20, help="Number of results")
):
    """Search for models."""
    results = thermal_search(query, limit)
    display_results(results)
```

## Deployment

The app is designed to be deployment-ready:

- Static files can be served from any web server
- API can run on any ASGI server (uvicorn, gunicorn)
- CLI works as a standalone tool

Remember: Keep it simple, fast, and thermal-aware!