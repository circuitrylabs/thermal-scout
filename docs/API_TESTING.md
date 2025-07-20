# API Testing Guide

This guide covers testing strategies and tools for the Thermal Scout API.

## Testing Tools

### 1. Interactive Documentation (Swagger UI)

Visit http://localhost:8080/docs for an interactive API explorer:

- Try out endpoints directly in the browser
- View request/response schemas
- Test with different parameters
- See example responses

### 2. cURL Examples

#### Health Check
```bash
curl -X GET "http://localhost:8080/health"
```

#### Search Models
```bash
# Basic search
curl -X GET "http://localhost:8080/api/v1/search?q=sentiment%20analysis"

# With parameters
curl -X GET "http://localhost:8080/api/v1/search?q=bert&limit=5&thermal_aware=true"

# Filter by type
curl -X GET "http://localhost:8080/api/v1/search?q=llama&model_type=text-generation"
```

#### Get Model Details
```bash
curl -X GET "http://localhost:8080/api/v1/models/distilbert-base-uncased"
```

### 3. HTTPie (User-Friendly Alternative to cURL)

Install HTTPie:
```bash
uv add --dev httpie
```

Examples:
```bash
# Health check
http GET localhost:8080/health

# Search
http GET localhost:8080/api/v1/search q=="sentiment analysis" limit==5

# Model details
http GET localhost:8080/api/v1/models/bert-base-uncased
```

### 4. Python Testing Script

Create `test_api_manual.py`:

```python
import requests
import json
from rich.console import Console
from rich.table import Table

console = Console()
BASE_URL = "http://localhost:8080"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    console.print(f"[green]Health Check:[/green] {response.json()}")
    assert response.status_code == 200

def test_search():
    """Test search endpoint"""
    params = {
        "q": "sentiment analysis",
        "limit": 5,
        "thermal_aware": True
    }
    response = requests.get(f"{BASE_URL}/api/v1/search", params=params)
    data = response.json()
    
    # Display results in a table
    table = Table(title="Search Results")
    table.add_column("Model ID", style="cyan")
    table.add_column("Thermal Cost", style="green")
    table.add_column("Downloads", justify="right")
    
    for model in data["models"]:
        table.add_row(
            model["modelId"],
            model["thermal_cost"],
            f"{model['downloads']:,}"
        )
    
    console.print(table)
    assert response.status_code == 200

def test_model_details():
    """Test model details endpoint"""
    model_id = "distilbert-base-uncased"
    response = requests.get(f"{BASE_URL}/api/v1/models/{model_id}")
    
    if response.status_code == 200:
        console.print(f"[green]Model Details:[/green]")
        console.print(json.dumps(response.json(), indent=2))
    else:
        console.print(f"[red]Error:[/red] {response.status_code}")

if __name__ == "__main__":
    console.print("[bold]Testing Thermal Scout API[/bold]\n")
    
    test_health()
    console.print()
    
    test_search()
    console.print()
    
    test_model_details()
```

Run with:
```bash
uv run python test_api_manual.py
```

### 5. Postman Collection

Import this collection into Postman:

```json
{
  "info": {
    "name": "Thermal Scout API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": "{{base_url}}/health"
      }
    },
    {
      "name": "Search Models",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/api/v1/search?q=sentiment analysis&limit=5",
          "host": ["{{base_url}}"],
          "path": ["api", "v1", "search"],
          "query": [
            {"key": "q", "value": "sentiment analysis"},
            {"key": "limit", "value": "5"},
            {"key": "thermal_aware", "value": "true", "disabled": true},
            {"key": "model_type", "value": "text-classification", "disabled": true}
          ]
        }
      }
    },
    {
      "name": "Get Model Details",
      "request": {
        "method": "GET",
        "header": [],
        "url": "{{base_url}}/api/v1/models/distilbert-base-uncased"
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8080"
    }
  ]
}
```

## Automated Testing

### Running Unit Tests

```bash
# Run all tests
uv run pytest

# Run only API tests
uv run pytest tests/test_api.py -v

# Run with coverage
uv run pytest --cov=thermal_scout tests/
```

### Load Testing with Locust

Install Locust:
```bash
uv add --dev locust
```

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class ThermalScoutUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def search_models(self):
        self.client.get("/api/v1/search?q=bert&limit=10")
    
    @task(1)
    def health_check(self):
        self.client.get("/health")
    
    @task(2)
    def get_model_details(self):
        self.client.get("/api/v1/models/distilbert-base-uncased")
```

Run load test:
```bash
# Start Locust web UI
uv run locust --host=http://localhost:8080

# Or run headless
uv run locust --host=http://localhost:8080 --headless -u 10 -r 2 -t 30s
```

## API Monitoring

### Health Check Script

Create `monitor_api.py`:

```python
import time
import requests
from datetime import datetime

def monitor_health(interval=60):
    """Monitor API health every interval seconds"""
    while True:
        try:
            response = requests.get("http://localhost:8080/health", timeout=5)
            status = "✅ UP" if response.status_code == 200 else "❌ DOWN"
            print(f"[{datetime.now()}] API Status: {status}")
        except Exception as e:
            print(f"[{datetime.now()}] API Status: ❌ ERROR - {e}")
        
        time.sleep(interval)

if __name__ == "__main__":
    monitor_health(30)  # Check every 30 seconds
```

## Testing Best Practices

### 1. Test Different Scenarios

- **Valid inputs**: Normal use cases
- **Edge cases**: Empty queries, maximum limits
- **Invalid inputs**: Missing parameters, wrong types
- **Error conditions**: Non-existent models

### 2. Performance Testing

```python
import time
import statistics

def benchmark_endpoint(url, n=100):
    """Benchmark an endpoint"""
    times = []
    
    for _ in range(n):
        start = time.time()
        requests.get(url)
        end = time.time()
        times.append(end - start)
    
    print(f"Average: {statistics.mean(times)*1000:.2f}ms")
    print(f"Median: {statistics.median(times)*1000:.2f}ms")
    print(f"95th percentile: {statistics.quantiles(times, n=20)[18]*1000:.2f}ms")
```

### 3. Contract Testing

Ensure API responses match expected schema:

```python
from jsonschema import validate

search_schema = {
    "type": "object",
    "properties": {
        "models": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["modelId", "thermal_cost"],
            }
        },
        "query": {"type": "string"},
        "limit": {"type": "integer"},
        "thermal_aware": {"type": "boolean"}
    },
    "required": ["models", "query", "limit", "thermal_aware"]
}

response = requests.get("http://localhost:8080/api/v1/search?q=bert")
validate(response.json(), search_schema)
```

## Debugging API Issues

### 1. Enable Debug Logging

```bash
# Run with debug logging
uv run uvicorn thermal_scout.api.main:app --log-level debug
```

### 2. Inspect Request/Response

```python
import logging
import httpx

logging.basicConfig(level=logging.DEBUG)

# This will show detailed request/response info
with httpx.Client() as client:
    response = client.get("http://localhost:8080/api/v1/search?q=bert")
```

### 3. Use API Middleware for Logging

Add to `api/main.py`:

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response
```

## Security Testing

### Check for Common Vulnerabilities

```bash
# SQL Injection attempt (should be safe)
curl "http://localhost:8080/api/v1/search?q='; DROP TABLE models;--"

# XSS attempt (should be escaped)
curl "http://localhost:8080/api/v1/search?q=<script>alert('xss')</script>"

# Path traversal (should be rejected)
curl "http://localhost:8080/api/v1/models/../../etc/passwd"
```

## Continuous Testing

### GitHub Actions Workflow

Add to `.github/workflows/test-api.yml`:

```yaml
name: API Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      
      - name: Install dependencies
        run: uv sync --extra dev
      
      - name: Start API
        run: |
          uv run uvicorn thermal_scout.api.main:app &
          sleep 5  # Wait for API to start
      
      - name: Run API tests
        run: uv run pytest tests/test_api.py -v
```

## Next Steps

1. Set up integration tests with real Hugging Face API
2. Add contract testing with Pact
3. Implement API versioning tests
4. Create performance benchmarks
5. Add security scanning with OWASP ZAP