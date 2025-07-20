# Thermal Scout 🔥

A thermal-aware Hugging Face model search and exploration tool with CLI and API interfaces.

## Features

- 🔍 **Smart Search**: Find AI models on Hugging Face Hub
- 🌡️ **Thermal Awareness**: Models sorted by computational efficiency (Low/Medium/High)
- 🚀 **Fast API**: RESTful API built with FastAPI
- 💻 **CLI Interface**: Beautiful terminal UI with Rich
- 📊 **Model Insights**: Downloads, likes, and task information

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd thermal-scout

# Install with uv
uv sync

# For development
uv sync --extra dev
```

## Usage

### 🖥️ CLI Interface

```bash
# Search with thermal awareness
uv run thermal-scout search "sentiment analysis" --limit 5

# Filter by model type
uv run thermal-scout search "llama" --type text-generation

# Disable thermal sorting
uv run thermal-scout search "bert" --no-thermal
```

### 🌐 API Server

Start the API server:

```bash
uv run python run_api.py
```

The API will be available at:
- Base URL: http://localhost:8080
- Interactive Docs: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

#### API Examples

```bash
# Search for models
curl "http://localhost:8080/api/v1/search?q=sentiment+analysis&limit=5"

# Get model details
curl "http://localhost:8080/api/v1/models/distilbert-base-uncased"

# Check health
curl "http://localhost:8080/health"
```

## Thermal Cost Indicators

Thermal Scout categorizes models based on their computational requirements:

| Indicator | Thermal Cost | Description | Examples |
|-----------|--------------|-------------|----------|
| 🟢 | Low | <1B parameters, efficient models | DistilBERT, TinyBERT |
| 🟡 | Medium | 1-3B parameters, moderate size | BERT-base, RoBERTa-base |
| 🔴 | High | >3B parameters, large models | GPT-3, LLaMA-7B |

## Documentation

- 📖 [API Reference](docs/API.md) - Complete API documentation
- 🛠️ [Local Development](docs/LOCAL_DEVELOPMENT.md) - Development setup guide
- 🧪 [API Testing Guide](docs/API_TESTING.md) - Testing strategies and tools

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=thermal_scout

# Run specific tests
uv run pytest tests/test_api.py -v
```

### Code Quality

```bash
# Lint and format
uv run ruff check --fix .
uv run ruff format .

# Type checking
uv run mypy thermal_scout/
```

### Pre-commit Hooks

```bash
# Install hooks
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests and linting
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- 🚀 Built with [FastAPI](https://fastapi.tiangolo.com/) and [Typer](https://typer.tiangolo.com/)
- 🤗 Powered by [Hugging Face Hub](https://huggingface.co/)
- 🎨 Beautiful CLI with [Rich](https://rich.readthedocs.io/)

---

Made with ❤️ by Claude and Tyler for sustainable AI