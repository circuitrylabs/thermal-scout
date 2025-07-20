# Thermal Scout User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Understanding Thermal Costs](#understanding-thermal-costs)
4. [Common Use Cases](#common-use-cases)
5. [Advanced Usage](#advanced-usage)
6. [Tips and Best Practices](#tips-and-best-practices)
7. [Troubleshooting](#troubleshooting)

## Introduction

Thermal Scout is your intelligent companion for discovering Hugging Face models while considering computational costs and energy efficiency. Whether you're running models on a laptop, in the cloud, or on edge devices, Thermal Scout helps you find models that match both your task requirements and hardware constraints.

### Why Thermal Awareness Matters

- **💰 Cost Savings**: Lower thermal footprint = lower cloud computing costs
- **🔋 Battery Life**: Efficient models extend battery life on laptops/mobile devices  
- **🌍 Environmental Impact**: Reduce carbon footprint by choosing efficient models
- **🚀 Performance**: Match models to your actual hardware capabilities

## Getting Started

### Installation

```bash
# Clone and enter the repository
git clone <repo-url>
cd thermal-scout

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

### Your First Search

Let's find an efficient model for sentiment analysis:

```bash
# Basic search with thermal awareness
uv run thermal-scout search "sentiment analysis" --limit 5

# You'll see output like:
# ┌─────────────────────────────────────┬──────────┬───────┬─────────┬──────────┐
# │ Model                               │ Downloads│ Likes │ Thermal │ Tags     │
# ├─────────────────────────────────────┼──────────┼───────┼─────────┼──────────┤
# │ distilbert-base-uncased            │  1234567 │  890  │ 🟢 Low  │ pytorch  │
# └─────────────────────────────────────┴──────────┴───────┴─────────┴──────────┘
```

## Understanding Thermal Costs

### Thermal Indicators

| Symbol | Category | Power Usage | Best For |
|--------|----------|-------------|----------|
| 🟢 | Low | < 10W | Laptops, edge devices, continuous operation |
| 🟡 | Medium | 10-50W | Workstations, occasional GPU use |
| 🔴 | High | 50-150W | Dedicated GPUs, batch processing |
| 🔥 | Very High | 150W+ | High-end GPUs, research/training |

### Real-World Examples

- **🟢 Low**: DistilBERT can run on a laptop CPU while on battery
- **🟡 Medium**: BERT-base benefits from GPU but works on good CPUs
- **🔴 High**: GPT-2 large requires GPU for reasonable performance
- **🔥 Very High**: Large LLMs need high-end GPUs with active cooling

## Common Use Cases

### 1. Finding Models for Limited Hardware

**Scenario**: You need NLP models for a laptop with 8GB RAM and no GPU.

```bash
# Get recommendations with thermal constraints
uv run thermal-scout recommend "text classification for emails" \
  --max-thermal low

# Analyze a specific efficient model
uv run thermal-scout analyze "distilbert-base-uncased"
```

### 2. Comparing Model Trade-offs

**Scenario**: Choosing between accuracy and efficiency for production deployment.

```bash
# Compare BERT variants
uv run thermal-scout compare \
  bert-base-uncased \
  distilbert-base-uncased \
  albert-base-v2

# Output shows size, speed, and thermal costs side-by-side
```

### 3. Exploring Models by Task

**Scenario**: You need models for specific NLP tasks with efficiency in mind.

```bash
# Text generation for creative writing
uv run thermal-scout search "text generation" \
  --type text-generation \
  --limit 10

# Question answering for customer support
uv run thermal-scout recommend "question answering for FAQs" \
  --max-thermal medium \
  --max-size 1GB
```

### 4. Managing Model Storage

**Scenario**: Check and manage cached models to free up disk space.

```bash
# Check cache status
uv run thermal-scout cache info

# List all cached models
uv run thermal-scout cache list

# Clear cache if needed
uv run thermal-scout cache clear
```

## Advanced Usage

### Combining Filters

Find models that match multiple criteria:

```bash
# Small, efficient models for mobile deployment
uv run thermal-scout recommend \
  "image classification for mobile app" \
  --max-thermal low \
  --max-size 500MB
```

### Programmatic Usage

Use Thermal Scout in your Python projects:

```python
from thermal_scout.search import thermal_search
from thermal_scout.analyzer import analyze_model

# Find efficient sentiment models
models = thermal_search("sentiment", limit=5, thermal_aware=True)

# Analyze the most efficient one
if models:
    best_model = models[0]  # Already sorted by thermal efficiency
    analysis = analyze_model(best_model['modelId'])
    
    print(f"Model: {analysis['model_id']}")
    print(f"Size: {analysis['size']}")
    print(f"Requirements: {analysis['requirements']}")
```

### Custom Workflows

Build model selection pipelines:

```python
from thermal_scout import search, analyzer, compare

def find_best_model_for_hardware(task, max_ram="16GB", has_gpu=False):
    # Set thermal limit based on hardware
    thermal_limit = "medium" if has_gpu else "low"
    
    # Get recommendations
    from thermal_scout.recommend import get_recommendations
    models = get_recommendations(
        task=task,
        max_thermal=thermal_limit,
        max_size=max_ram
    )
    
    # Analyze top 3
    results = []
    for model in models[:3]:
        analysis = analyzer.analyze_model(model['model_id'])
        results.append({
            'model': model['model_id'],
            'thermal': analysis['thermal_footprint'],
            'requirements': analysis['requirements']
        })
    
    return results
```

## Tips and Best Practices

### 1. Start with Thermal Awareness

Always begin searches with thermal awareness enabled (default). You can disable it with `--no-thermal` if needed, but this helps discover efficient models first.

### 2. Use Task-Specific Searches

Be specific about your task for better recommendations:

```bash
# Good: Specific task and domain
uv run thermal-scout recommend "sentiment analysis for product reviews"

# Less effective: Too generic
uv run thermal-scout search "nlp model"
```

### 3. Consider the Full Stack

Remember that thermal costs compound:
- Running 10 efficient models might use less power than 1 large model
- Batch processing can be more efficient than continuous inference
- CPU-optimized models might be better for always-on services

### 4. Test Before Deploying

Always verify model performance on your target hardware:

```bash
# 1. Find candidate models
uv run thermal-scout recommend "your task" --max-thermal low

# 2. Analyze requirements
uv run thermal-scout analyze "model-name"

# 3. Test with small batches before full deployment
```

### 5. Monitor Cache Size

Large models can quickly fill disk space:

```bash
# Regular maintenance
uv run thermal-scout cache info  # Check monthly
uv run thermal-scout cache clear # When needed
```

## Troubleshooting

### Common Issues

**"No models found"**
- Try broader search terms
- Increase the thermal limit
- Remove size constraints

**"Import error"**
- Ensure all dependencies are installed: `uv sync`
- Check Python version: requires 3.12+

**"API rate limit"**
- Thermal Scout caches results automatically
- Wait a few minutes between large searches
- Use more specific queries to reduce API calls

### Performance Tips

1. **Use specific model types**: Add `--type` to filter results
2. **Batch operations**: Compare multiple models in one command
3. **Cache warming**: Search for common models to populate cache

### Getting Help

1. Check the API Reference: `docs/API_REFERENCE.md`
2. Review examples: `examples/quick_start.py`
3. Explore the codebase: Well-documented Python modules

## Next Steps

- Explore the [API Reference](API_REFERENCE.md) for programmatic usage
- Read the [Architecture Guide](ARCHITECTURE.md) to understand internals
- Check the [Changelog](../CHANGELOG.md) for latest updates

Remember: The most powerful model isn't always the best choice. Thermal Scout helps you find the sweet spot between capability and efficiency! 🚀