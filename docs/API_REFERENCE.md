# Thermal Scout API Reference

## Overview

Thermal Scout provides a Python API for thermal-aware Hugging Face model discovery and analysis. This reference covers all public functions and their usage.

## Core Modules

### `thermal_scout.search`

#### `thermal_search(query, limit=10, model_type=None, thermal_aware=True)`

Search Hugging Face Hub for models with optional thermal awareness.

**Parameters:**
- `query` (str): Search query for models
- `limit` (int): Maximum number of results to return (default: 10)
- `model_type` (str, optional): Filter by model type (e.g., "text-generation", "text-classification")
- `thermal_aware` (bool): Enable thermal cost filtering and ranking (default: True)

**Returns:**
- `List[Dict[str, Any]]`: List of model dictionaries containing:
  - `modelId` (str): Hugging Face model identifier
  - `downloads` (int): Download count
  - `likes` (int): Number of likes
  - `tags` (List[str]): Model tags
  - `pipeline_tag` (str): Model pipeline type
  - `library_name` (str): Framework (pytorch, tensorflow, etc.)
  - `thermal_cost` (str): Thermal indicator ("🟢 Low", "🟡 Medium", "🔴 High")

**Example:**
```python
from thermal_scout.search import thermal_search

# Search for efficient sentiment models
results = thermal_search(
    "sentiment analysis", 
    limit=5,
    model_type="text-classification",
    thermal_aware=True
)

for model in results:
    print(f"{model['modelId']}: {model['thermal_cost']}")
```

#### `estimate_thermal_cost(model_info)`

Estimate the thermal cost of a model based on its characteristics.

**Parameters:**
- `model_info` (Dict[str, Any]): Model information dictionary

**Returns:**
- `str`: Thermal cost indicator ("🟢 Low", "🟡 Medium", "🔴 High")

**Thermal Scoring Algorithm:**
1. Checks model ID for size indicators (tiny, small, base, large, xl, xxl)
2. Searches for parameter count patterns (e.g., "7B", "350M")
3. Adjusts score based on efficiency tags ("distil", "efficient", "tiny")
4. Maps final score to thermal categories

---

### `thermal_scout.analyzer`

#### `analyze_model(model_id, include_embeddings=False)`

Analyze a model's characteristics and thermal footprint.

**Parameters:**
- `model_id` (str): Hugging Face model identifier
- `include_embeddings` (bool): Generate sample embeddings (default: False)

**Returns:**
- `Dict[str, Any]`: Analysis results containing:
  - `model_id` (str): Model identifier
  - `size` (str): Model size in human-readable format
  - `parameters` (str): Parameter count if available
  - `architecture` (str): Model architecture type
  - `thermal_footprint` (str): Thermal cost with typical power consumption
  - `requirements` (Dict[str, str]): Hardware requirements
    - `RAM`: Recommended system memory
    - `VRAM`: GPU memory requirements
    - `Compute`: CPU/GPU recommendations
  - `pipeline_tag` (str): Model pipeline type
  - `library` (str): Framework used
  - `sample_embedding` (List[float], optional): Sample embedding vector

**Example:**
```python
from thermal_scout.analyzer import analyze_model

analysis = analyze_model("distilbert-base-uncased")
print(f"Size: {analysis['size']}")
print(f"Thermal: {analysis['thermal_footprint']}")
print(f"Requirements: {analysis['requirements']}")
```

#### Helper Functions

- `parse_model_size(model_info)`: Extract size information from model metadata
- `estimate_requirements(size_info, model_info)`: Calculate hardware requirements
- `calculate_thermal_footprint(size_info, architecture)`: Determine thermal category

---

### `thermal_scout.compare`

#### `compare_models(model_ids)`

Compare multiple models side-by-side.

**Parameters:**
- `model_ids` (List[str]): List of Hugging Face model identifiers

**Returns:**
- `Dict[str, Dict[str, Any]]`: Dictionary mapping model IDs to comparison data:
  - `size` (str): Model size
  - `parameters` (str): Parameter count
  - `thermal_cost` (str): Thermal indicator
  - `memory_required` (str): RAM requirements
  - `inference_speed` (str): Speed indicator ("⚡ Fast", "🏃 Moderate", "🚶 Slow", "🐌 Very Slow")
  - `architecture` (str): Model architecture
  - `pipeline` (str): Pipeline type

**Example:**
```python
from thermal_scout.compare import compare_models

comparison = compare_models([
    "bert-base-uncased",
    "distilbert-base-uncased",
    "albert-base-v2"
])

for model_id, data in comparison.items():
    print(f"{model_id}: {data['thermal_cost']} - {data['inference_speed']}")
```

---

### `thermal_scout.recommend`

#### `get_recommendations(task, max_thermal="medium", max_size=None)`

Get model recommendations based on task and constraints.

**Parameters:**
- `task` (str): Task description (e.g., "text generation for stories")
- `max_thermal` (str): Maximum thermal cost ("low", "medium", "high") (default: "medium")
- `max_size` (str, optional): Maximum model size (e.g., "7B", "1GB")

**Returns:**
- `List[Dict[str, Any]]`: Ordered list of recommendations:
  - `model_id` (str): Model identifier
  - `thermal_cost` (str): Thermal indicator
  - `size` (str): Model size (if available)
  - `score` (float): Relevance score
  - `reason` (str): Human-readable recommendation reason

**Task Mappings:**
The system recognizes common NLP tasks and maps them to model types:
- "text generation" → text-generation, text2text-generation
- "classification" → text-classification, zero-shot-classification
- "question answering" → question-answering
- "summarization" → summarization, text2text-generation
- "translation" → translation, text2text-generation
- "embedding" → feature-extraction, sentence-similarity
- "code" → text-generation, code
- "chat" → text-generation, conversational
- "sentiment" → text-classification, sentiment-analysis
- "ner" → token-classification, ner

**Example:**
```python
from thermal_scout.recommend import get_recommendations

# Get efficient models for creative writing
recommendations = get_recommendations(
    task="text generation for creative writing",
    max_thermal="medium",
    max_size="7B"
)

for rec in recommendations[:3]:
    print(f"{rec['model_id']}: {rec['reason']}")
```

#### Helper Functions

- `parse_size_constraint(max_size)`: Parse size strings to numeric values
- `infer_model_types(task)`: Extract model types from task description
- `filter_by_thermal(models, max_thermal)`: Filter models by thermal constraint
- `score_model_for_task(model, task, task_types)`: Calculate task relevance score

---

### `thermal_scout.cache`

#### `manage_cache(action)`

Manage the Hugging Face model cache.

**Parameters:**
- `action` (str): Cache action to perform
  - `"clear"`: Clear the entire cache
  - `"info"`: Get cache information
  - `"list"`: List cached models

**Returns:**
- For `"clear"`: String message with cleared size
- For `"info"`: Dictionary with:
  - `location` (str): Cache directory path
  - `size` (str): Total cache size
  - `model_count` (int): Number of cached models
  - `warnings` (int): Number of cache warnings
- For `"list"`: List of cached model strings with sizes

**Example:**
```python
from thermal_scout.cache import manage_cache

# Check cache status
info = manage_cache("info")
print(f"Cache size: {info['size']}")
print(f"Models cached: {info['model_count']}")

# List cached models
models = manage_cache("list")
for model in models:
    print(model)

# Clear cache (use with caution!)
result = manage_cache("clear")
print(result)
```

---

## Data Structures

### Model Information Dictionary

```python
{
    "modelId": "distilbert-base-uncased",
    "downloads": 1234567,
    "likes": 890,
    "tags": ["transformers", "pytorch", "bert"],
    "pipeline_tag": "text-classification",
    "library_name": "transformers",
    "thermal_cost": "🟢 Low"
}
```

### Analysis Result Dictionary

```python
{
    "model_id": "distilbert-base-uncased",
    "size": "250 MB",
    "parameters": "66M parameters",
    "architecture": "text-classification",
    "thermal_footprint": "🟢 Low (< 10W typical)",
    "requirements": {
        "RAM": "8 GB",
        "VRAM": "6 GB (GPU optional)",
        "Compute": "CPU is sufficient"
    },
    "pipeline_tag": "text-classification",
    "library": "transformers"
}
```

### Recommendation Dictionary

```python
{
    "model_id": "gpt2",
    "thermal_cost": "🟡 Medium",
    "size": "Check model card",
    "score": 2.5,
    "reason": "Excellent match for task type - balanced performance"
}
```

---

## Error Handling

All functions handle errors gracefully and return appropriate error dictionaries:

```python
{
    "error": "Model 'invalid-model-id' not found on Hugging Face Hub"
}
```

Functions will not raise exceptions for network errors or missing models, instead returning empty lists or error dictionaries.

---

## Thermal Cost Categories

| Indicator | Power Range | Description |
|-----------|-------------|-------------|
| 🟢 Low | < 10W | Energy efficient, suitable for CPU inference |
| 🟡 Medium | 10-50W | Balanced performance, GPU recommended |
| 🔴 High | 50-150W | Performance-focused, GPU required |
| 🔥 Very High | 150W+ | Resource intensive, high-end GPU required |

---

## Best Practices

1. **Use Thermal Awareness**: Keep `thermal_aware=True` for energy-efficient model discovery
2. **Set Appropriate Limits**: Use reasonable `limit` values to avoid excessive API calls
3. **Cache Management**: Periodically check cache size with `manage_cache("info")`
4. **Task Descriptions**: Provide clear, specific task descriptions for better recommendations
5. **Size Constraints**: Use size constraints to filter out models that won't fit your hardware

---

## Integration Examples

### Building a Model Selection Pipeline

```python
from thermal_scout import search, analyzer, recommend

# Step 1: Get recommendations for your task
recommendations = recommend.get_recommendations(
    task="sentiment analysis for product reviews",
    max_thermal="medium"
)

# Step 2: Analyze top candidates
for rec in recommendations[:3]:
    analysis = analyzer.analyze_model(rec['model_id'])
    print(f"\n{rec['model_id']}:")
    print(f"  Thermal: {analysis['thermal_footprint']}")
    print(f"  Size: {analysis['size']}")
    print(f"  Requirements: {analysis['requirements']['RAM']}")
```

### Thermal-Aware Model Discovery

```python
from thermal_scout import search, compare

# Find efficient text generation models
models = search.thermal_search(
    "text generation",
    limit=10,
    model_type="text-generation",
    thermal_aware=True
)

# Compare top 3 by thermal cost
model_ids = [m['modelId'] for m in models[:3]]
comparison = compare.compare_models(model_ids)

# Display comparison
for model_id, data in comparison.items():
    print(f"{model_id}: {data['thermal_cost']} - {data['memory_required']}")
```