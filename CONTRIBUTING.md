# Contributing to Thermal Scout

Thank you for your interest in contributing to Thermal Scout! This guide will help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/thermal-scout.git
   cd thermal-scout
   ```
3. Set up development environment:
   ```bash
   uv venv
   uv sync --extra dev
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clean, readable code
- Add type hints to all functions
- Follow existing patterns
- Keep changes focused

### 3. Run Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=thermal_scout
```

### 4. Format and Lint

```bash
# Format code
uv run ruff format .

# Check linting
uv run ruff check .

# Type check
uv run ty
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature"
```

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Maintenance tasks

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Code Standards

### Python

- Python 3.12+ required
- Type hints for all functions
- Docstrings for public functions
- 88 character line limit (ruff default)

Example:
```python
def search_models(query: str, limit: int = 20) -> list[dict[str, Any]]:
    """Search HuggingFace models.
    
    Args:
        query: Search query string
        limit: Maximum results to return
        
    Returns:
        List of model dictionaries
    """
    ...
```

### JavaScript

- ES6+ syntax
- No external dependencies
- Module pattern for organization
- Clear variable names

Example:
```javascript
function getThermalIndicator(parameters) {
    // Clear logic with early returns
    if (parameters < 1e9) return 'Cool';
    if (parameters < 3e9) return 'Warm';
    if (parameters < 7e9) return 'Moderate';
    return 'Hot';
}
```

## Testing

### Writing Tests

- Place tests in `tests/` directory
- Mirror source structure
- Use descriptive test names
- Test edge cases

Example:
```python
def test_thermal_indicator_cool():
    """Test thermal indicator for cool models."""
    assert get_thermal_indicator(500_000_000) == "Cool"
```

### Running Tests

```bash
# Specific test file
uv run pytest tests/test_search.py

# Specific test
uv run pytest tests/test_search.py::test_thermal_indicator

# With debugging
uv run pytest -vv --tb=short
```

## Documentation

- Update README.md for user-facing changes
- Update API.md for API changes
- Add docstrings to new functions
- Include examples where helpful

## Pull Request Guidelines

### Before Submitting

- [ ] Tests pass (`uv run pytest`)
- [ ] Code is formatted (`uv run ruff format .`)
- [ ] Linting passes (`uv run ruff check .`)
- [ ] Type checking passes (`uv run ty`)
- [ ] Documentation updated
- [ ] Commit messages follow convention

### PR Description

Include:
- What changes were made
- Why they were made
- Any breaking changes
- Screenshots for UI changes

## Development Tips

### Local Testing

```bash
# Test web UI
python -m http.server 8000

# Test CLI
uv run python -m thermal_scout.cli search "llama"

# Test API
uv run python run_api.py
```

### Debugging

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use breakpoints
import pdb; pdb.set_trace()
```

## Architecture Decisions

- **Minimal dependencies**: Keep the project lightweight
- **Type safety**: Use type hints everywhere
- **Simple is better**: Prefer clarity over cleverness
- **Test coverage**: Maintain >95% coverage

## Getting Help

- Open an issue for bugs
- Start a discussion for features
- Ask questions in issues
- Check existing issues first

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

Thank you for contributing to Thermal Scout! 🔥