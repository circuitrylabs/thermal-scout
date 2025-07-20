# Thermal Scout API Reference

A thermal-aware Hugging Face model search API built with FastAPI.

## Base URL

```
http://localhost:8080
```

## Authentication

Currently, the API is open and does not require authentication. Future versions may add API key support for rate limiting.

## Endpoints

### Health Check

Check if the API is running and healthy.

```http
GET /health
```

#### Response

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "thermal_aware": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| status | string | Service health status |
| version | string | API version |
| thermal_aware | boolean | Whether thermal awareness is enabled |

---

### Search Models

Search for models on Hugging Face Hub with thermal-aware sorting.

```http
GET /api/v1/search
```

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| q | string | Yes | - | Search query for models |
| limit | integer | No | 10 | Number of results (1-100) |
| model_type | string | No | null | Filter by model type/task |
| thermal_aware | boolean | No | true | Enable thermal-aware sorting |

#### Example Requests

```bash
# Basic search
curl "http://localhost:8080/api/v1/search?q=sentiment+analysis"

# Search with limit
curl "http://localhost:8080/api/v1/search?q=bert&limit=5"

# Filter by model type
curl "http://localhost:8080/api/v1/search?q=llama&model_type=text-generation"

# Disable thermal sorting
curl "http://localhost:8080/api/v1/search?q=gpt&thermal_aware=false"
```

#### Response

```json
{
  "models": [
    {
      "modelId": "distilbert-base-uncased",
      "downloads": 1000000,
      "likes": 500,
      "tags": ["transformers", "pytorch", "bert", "distilled"],
      "pipeline_tag": "text-classification",
      "library_name": "transformers",
      "thermal_cost": "Low"
    }
  ],
  "query": "sentiment analysis",
  "limit": 10,
  "thermal_aware": true
}
```

#### Model Object

| Field | Type | Description |
|-------|------|-------------|
| modelId | string | Unique model identifier |
| downloads | integer | Number of downloads |
| likes | integer | Number of likes |
| tags | array[string] | Model tags |
| pipeline_tag | string/null | Model task type |
| library_name | string/null | ML library used |
| thermal_cost | string | Thermal efficiency: "Low", "Medium", or "High" |

---

### Get Model Details

Get detailed information about a specific model.

```http
GET /api/v1/models/{model_id}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| model_id | string | The model ID (e.g., bert-base-uncased) |

#### Example Request

```bash
curl "http://localhost:8080/api/v1/models/distilbert-base-uncased"
```

#### Response

```json
{
  "modelId": "distilbert-base-uncased",
  "thermal_cost": "Low",
  "downloads": 1000000,
  "likes": 500,
  "tags": ["transformers", "pytorch", "bert", "distilled"],
  "pipeline_tag": "text-classification",
  "library_name": "transformers",
  "description": null
}
```

---

## Thermal Cost Indicators

The API automatically calculates thermal cost based on model characteristics:

| Thermal Cost | Description | Examples |
|--------------|-------------|----------|
| **Low** 🟢 | Small, efficient models (<1B parameters) | TinyBERT, DistilBERT, MobileBERT |
| **Medium** 🟡 | Moderate size models (1-3B parameters) | BERT-base, RoBERTa-base, GPT-2 |
| **High** 🔴 | Large models requiring significant compute (3B+ parameters) | GPT-3, LLaMA, BLOOM |

## Error Responses

The API uses standard HTTP status codes and returns errors in a consistent format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 404 | Model not found |
| 422 | Validation error (missing/invalid parameters) |
| 500 | Internal server error |

## Rate Limiting

Currently no rate limiting is implemented. In production, consider adding rate limits per IP or API key.

## CORS

The API supports CORS for the following origins:
- `http://localhost:8000` (Frontend development)
- `http://localhost:3000` (Alternative frontend port)
- `*` (All origins - for development only)

## Interactive Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## SDK Usage Examples

### Python

```python
import requests

# Search for models
response = requests.get(
    "http://localhost:8080/api/v1/search",
    params={"q": "sentiment analysis", "limit": 5}
)
models = response.json()["models"]

# Get model details
model_id = models[0]["modelId"]
details = requests.get(f"http://localhost:8080/api/v1/models/{model_id}").json()
```

### JavaScript

```javascript
// Search for models
const response = await fetch(
  "http://localhost:8080/api/v1/search?q=sentiment+analysis&limit=5"
);
const data = await response.json();

// Get model details
const modelId = data.models[0].modelId;
const details = await fetch(
  `http://localhost:8080/api/v1/models/${modelId}`
).then(r => r.json());
```

## WebSocket Support (Future)

Future versions may include WebSocket support for real-time model updates and streaming search results.