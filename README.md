# Thermal Scout

A thermal-aware Hugging Face model search and exploration CLI buddy that helps you find the right models while considering computational costs and energy efficiency.

## Features

- **Smart Search**: Search Hugging Face Hub with thermal cost awareness
- **Model Analysis**: Analyze models' characteristics and thermal footprint
- **Comparison**: Compare multiple models side-by-side
- **Recommendations**: Get model suggestions based on task and constraints
- **Cache Management**: Manage your local Hugging Face model cache

## Installation

```bash
# Clone the repository
cd thermal-scout

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

## Quick Start

### Search for Models

```bash
# Basic search with thermal awareness
uv run thermal-scout search "sentiment analysis" --limit 5

# Search for specific model types
uv run thermal-scout search "text generation" --type text-generation --limit 10

# Search without thermal filtering
uv run thermal-scout search "bert" --no-thermal
```

### Analyze a Model

```bash
# Basic analysis
uv run thermal-scout analyze "distilbert-base-uncased"

# Include embedding analysis
uv run thermal-scout analyze "sentence-transformers/all-MiniLM-L6-v2" --embeddings
```

### Compare Models

```bash
# Compare multiple models
uv run thermal-scout compare bert-base-uncased roberta-base distilbert-base-uncased
```

### Get Recommendations

```bash
# Get recommendations for a task
uv run thermal-scout recommend "text generation for creative writing"

# With thermal constraints
uv run thermal-scout recommend "question answering" --max-thermal medium

# With size constraints
uv run thermal-scout recommend "code generation" --max-size 7B
```

### Manage Cache

```bash
# View cache information
uv run thermal-scout cache info

# List cached models
uv run thermal-scout cache list

# Clear the cache
uv run thermal-scout cache clear
```

## Thermal Cost Indicators

- **Low**: Energy efficient models (< 10W typical)
- **Medium**: Balanced performance (10-50W typical)
- **High**: Performance-focused (50-150W typical)
- **Very High**: Resource intensive (150W+ typical)

## Examples

Run the quick start examples:

```bash
python examples/quick_start.py
```

## Development

The project uses UV for dependency management:

```bash
# Add a new dependency
uv add package-name

# Update dependencies
uv sync

# Run in development
uv run thermal-scout --help
```

## Architecture

- `thermal_scout/cli.py` - Main CLI interface using Typer
- `thermal_scout/search.py` - Thermal-aware model search
- `thermal_scout/analyzer.py` - Model analysis and footprint estimation
- `thermal_scout/compare.py` - Model comparison functionality
- `thermal_scout/recommend.py` - Task-based recommendations
- `thermal_scout/cache.py` - Cache management utilities

## Contributing

Feel free to open issues or submit pull requests to improve thermal awareness and model discovery!