# Thermal Scout API Reference

## Overview

Thermal Scout provides a REST API for searching AI models with thermal cost awareness. The API is built with FastAPI and follows RESTful principles.

## Base URL

```
http://localhost:8080
```

## Authentication

No authentication required. The API directly accesses HuggingFace Hub without API keys.

## Endpoints

### Health Check

```http
GET /health
```

Returns API health status.

**Response**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### Search Models

```http
GET /api/v1/search
```

Search for models on HuggingFace Hub with thermal awareness.

**Query Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| q | string | required | Search query |
| limit | integer | 20 | Number of results (1-100) |
| thermal | string | null | Filter by thermal level: cool, warm, moderate, hot |
| sort_by | string | relevance | Sort by: relevance, downloads, likes, thermal |

**Example Request**
```bash
curl "http://localhost:8080/api/v1/search?q=llama&limit=10&thermal=cool"
```

**Response**
```json
{
  "query": "llama",
  "total": 150,
  "results": [
    {
      "id": "meta-llama/Llama-2-7b",
      "task": "text-generation",
      "parameters": 7000000000,
      "thermal": {
        "level": "hot",
        "indicator": "🔴",
        "power_estimate": "150W+"
      },
      "downloads": 1234567,
      "likes": 890,
      "url": "https://huggingface.co/meta-llama/Llama-2-7b"
    }
  ]
}
```

### Get Model Details

```http
GET /api/v1/models/{model_id}
```

Get detailed information about a specific model.

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| model_id | string | Model ID (e.g., "meta-llama/Llama-2-7b") |

**Example Request**
```bash
curl "http://localhost:8080/api/v1/models/meta-llama/Llama-2-7b"
```

**Response**
```json
{
  "id": "meta-llama/Llama-2-7b",
  "task": "text-generation",
  "parameters": 7000000000,
  "thermal": {
    "level": "hot",
    "indicator": "🔴",
    "power_estimate": "150W+",
    "hardware_recommendation": "High-end GPU (RTX 4090, A100)"
  },
  "metrics": {
    "downloads": 1234567,
    "likes": 890
  },
  "tags": ["llama", "text-generation", "pytorch"],
  "created_at": "2023-07-18T00:00:00Z",
  "url": "https://huggingface.co/meta-llama/Llama-2-7b"
}
```

## Response Formats

### Thermal Levels

Models are categorized into four thermal levels:

| Level | Indicator | Parameters | Power Estimate |
|-------|-----------|------------|----------------|
| cool | 🟢 | <1B | 5-10W |
| warm | 🟡 | 1-3B | 10-50W |
| moderate | 🟠 | 3-7B | 50-150W |
| hot | 🔴 | 7B+ | 150W+ |

### Error Responses

All errors follow a consistent format:

```json
{
  "detail": "Error message",
  "status_code": 400
}
```

**Common Error Codes**

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Model not found |
| 429 | Too Many Requests - Rate limited |
| 500 | Internal Server Error |

## Rate Limiting

- No rate limiting on the API itself
- HuggingFace Hub may apply its own rate limits
- Responses are cached for 5 minutes

## Python Client Example

```python
import httpx

async def search_models(query: str, thermal: str = None):
    async with httpx.AsyncClient() as client:
        params = {"q": query}
        if thermal:
            params["thermal"] = thermal
        
        response = await client.get(
            "http://localhost:8080/api/v1/search",
            params=params
        )
        return response.json()

# Usage
results = await search_models("bert", thermal="cool")
```

## JavaScript Client Example

```javascript
async function searchModels(query, thermal) {
    const params = new URLSearchParams({ q: query });
    if (thermal) params.append('thermal', thermal);
    
    const response = await fetch(
        `http://localhost:8080/api/v1/search?${params}`
    );
    return response.json();
}

// Usage
const results = await searchModels('bert', 'cool');
```

## CLI Integration

The API powers the Thermal Scout CLI:

```bash
# Search via CLI (uses API internally)
thermal-scout search "llama" --thermal cool

# Direct API call
curl "http://localhost:8080/api/v1/search?q=llama&thermal=cool"
```

## Deployment

### Running Locally

```bash
# Development
uv run python run_api.py

# Production
uv run uvicorn thermal_scout.api.main:app --host 0.0.0.0 --port 8080
```

### Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["uvicorn", "thermal_scout.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| PORT | 8080 | API server port |
| LOG_LEVEL | INFO | Logging level |
| CACHE_TTL | 300 | Cache TTL in seconds |

## OpenAPI Documentation

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`
- OpenAPI JSON: `http://localhost:8080/openapi.json`