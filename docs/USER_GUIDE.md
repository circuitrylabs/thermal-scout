# Thermal Scout User Guide

## Quick Start

Thermal Scout helps you find AI models based on their computational "thermal" cost. Choose your interface:

### Web Interface

```bash
python -m http.server 8000
open http://localhost:8000
```

### Command Line

```bash
uv pip install -e .
thermal-scout search "llama"
```

### API

```bash
uv run python run_api.py
# API docs at http://localhost:8080/docs
```

## Understanding Thermal Costs

Models are categorized by computational requirements:

| Indicator | Level | Parameters | Use Case |
|-----------|-------|------------|----------|
| 🟢 | Cool | <1B | Edge devices, continuous operation |
| 🟡 | Warm | 1-3B | Workstations, batch processing |
| 🟠 | Moderate | 3-7B | Dedicated ML workstations |
| 🔴 | Hot | 7B+ | Data centers, research clusters |

## Using the Web Interface

1. **Open the app**: Navigate to http://localhost:8000
2. **Search models**: Enter keywords like "bert", "llama", or "stable-diffusion"
3. **View results**: See models with thermal indicators
4. **Click models**: Links go directly to HuggingFace

### Search Tips

- Use specific terms: "text generation" instead of "AI"
- Try model names: "bert", "gpt2", "t5"
- Search by task: "sentiment analysis", "image classification"

## Using the CLI

### Basic Search

```bash
# Simple search
thermal-scout search "bert"

# Limit results
thermal-scout search "llama" --limit 10

# Filter by thermal level
thermal-scout search "gpt" --thermal cool
```

### Output Formats

```bash
# Default table view
thermal-scout search "bert"

# JSON output for scripts
thermal-scout search "bert" --output json
```

### Examples

```bash
# Find cool models for edge devices
thermal-scout search "text classification" --thermal cool

# Search for specific tasks
thermal-scout search "question answering" --limit 5

# Get JSON for automation
thermal-scout search "bert" --output json | jq '.results[0]'
```

## Using the API

### Basic Request

```bash
# Search models
curl "http://localhost:8080/api/v1/search?q=bert&limit=5"

# Filter by thermal
curl "http://localhost:8080/api/v1/search?q=llama&thermal=cool"
```

### Python Example

```python
import requests

# Search for models
response = requests.get(
    "http://localhost:8080/api/v1/search",
    params={"q": "bert", "thermal": "cool", "limit": 10}
)
models = response.json()

# Process results
for model in models["results"]:
    print(f"{model['id']}: {model['thermal']['indicator']}")
```

### JavaScript Example

```javascript
// Search for models
fetch('http://localhost:8080/api/v1/search?q=bert&thermal=cool')
    .then(res => res.json())
    .then(data => {
        data.results.forEach(model => {
            console.log(`${model.id}: ${model.thermal.indicator}`);
        });
    });
```

## Common Use Cases

### Finding Models for Limited Hardware

```bash
# For CPU-only systems
thermal-scout search "text generation" --thermal cool

# For small GPUs
thermal-scout search "image classification" --thermal warm
```

### Comparing Model Efficiency

Look at the thermal indicators to compare models:
- Multiple cool models vs one hot model
- Trade-offs between size and capability
- Power consumption estimates

### Building Applications

Use the API to:
- Filter models by thermal cost in your app
- Display thermal awareness to users
- Make environmentally conscious choices

## Tips

1. **Start with cool models**: Try smaller models first
2. **Be specific**: Use task names for better results
3. **Check parameters**: Model size correlates with thermal cost
4. **Consider your hardware**: Match thermal level to your setup

## Troubleshooting

### No results found
- Try broader search terms
- Remove thermal filters
- Check your internet connection

### Slow searches
- First search may be slower
- Results are cached for 5 minutes
- API has no rate limits

### Installation issues
- Requires Python 3.12+
- Use `uv` for best results
- Check [CONTRIBUTING.md](../CONTRIBUTING.md) for setup

## Learn More

- [API Reference](API.md) - Full API documentation
- [Contributing](../CONTRIBUTING.md) - How to contribute
- [GitHub](https://github.com/circuitrylabs/thermal-scout) - Source code

Remember: Choose models that match your computational resources! 🔥