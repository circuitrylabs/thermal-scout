"""
FastAPI application for Thermal Scout API

Created with ❤️ by Claude and Tyler
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from thermal_scout.search import thermal_search

# Create FastAPI app
app = FastAPI(
    title="Thermal Scout API",
    description="A thermal-aware Hugging Face model search API",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check operations",
        },
        {
            "name": "search",
            "description": "Model search operations",
        },
        {
            "name": "models",
            "description": "Individual model operations",
        },
    ],
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class HealthResponse(BaseModel):
    status: str
    version: str
    thermal_aware: bool


class ModelInfo(BaseModel):
    modelId: str
    downloads: int
    likes: int
    tags: list[str]
    pipeline_tag: str | None = None
    library_name: str | None = None
    thermal_cost: str

    class Config:
        json_schema_extra = {
            "example": {
                "modelId": "distilbert-base-uncased",
                "downloads": 1000000,
                "likes": 500,
                "tags": ["transformers", "pytorch", "bert", "distilled"],
                "pipeline_tag": "text-classification",
                "library_name": "transformers",
                "thermal_cost": "Low",
            }
        }


class SearchResponse(BaseModel):
    models: list[ModelInfo]
    query: str
    limit: int
    thermal_aware: bool


class ModelDetailsResponse(BaseModel):
    modelId: str
    thermal_cost: str
    downloads: int
    likes: int
    tags: list[str]
    pipeline_tag: str | None = None
    library_name: str | None = None
    description: str | None = None


# Health check endpoint
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["health"],
    summary="Health Check",
    response_description="API health status",
)
async def health_check():
    """Check if the API is healthy and running"""
    return HealthResponse(status="healthy", version="0.1.0", thermal_aware=True)


# Search endpoint
@app.get(
    "/api/v1/search",
    response_model=SearchResponse,
    tags=["search"],
    summary="Search Models",
    response_description="List of models matching search criteria",
    responses={
        200: {
            "description": "Successful search",
            "content": {
                "application/json": {
                    "example": {
                        "models": [
                            {
                                "modelId": "distilbert-base-uncased",
                                "downloads": 1000000,
                                "likes": 500,
                                "tags": ["transformers", "bert"],
                                "pipeline_tag": "text-classification",
                                "library_name": "transformers",
                                "thermal_cost": "Low",
                            }
                        ],
                        "query": "sentiment analysis",
                        "limit": 10,
                        "thermal_aware": True,
                    }
                }
            },
        },
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
)
async def search_models(
    q: str = Query(
        ..., description="Search query for models", example="sentiment analysis"
    ),
    limit: int = Query(
        10, ge=1, le=100, description="Number of results to return", example=5
    ),
    model_type: str | None = Query(
        None, description="Filter by model type/task", example="text-classification"
    ),
    thermal_aware: bool = Query(
        True, description="Enable thermal-aware sorting", example=True
    ),
):
    """
    Search for models on Hugging Face Hub with thermal awareness

    - **q**: Search query (required)
    - **limit**: Number of results (1-100, default: 10)
    - **model_type**: Filter by model type (e.g., text-generation, text-classification)
    - **thermal_aware**: Sort by thermal efficiency (default: true)
    """
    try:
        results = thermal_search(
            query=q, limit=limit, model_type=model_type, thermal_aware=thermal_aware
        )

        # Convert to Pydantic models
        models = [
            ModelInfo(
                modelId=model["modelId"],
                downloads=model.get("downloads", 0),
                likes=model.get("likes", 0),
                tags=model.get("tags", []),
                pipeline_tag=model.get("pipeline_tag"),
                library_name=model.get("library_name"),
                thermal_cost=model.get("thermal_cost", "Unknown"),
            )
            for model in results
        ]

        return SearchResponse(
            models=models, query=q, limit=limit, thermal_aware=thermal_aware
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# Model details endpoint
@app.get(
    "/api/v1/models/{model_id:path}",
    response_model=ModelDetailsResponse,
    tags=["models"],
    summary="Get Model Details",
    response_description="Detailed information about a specific model",
    responses={
        200: {
            "description": "Model found",
            "content": {
                "application/json": {
                    "example": {
                        "modelId": "distilbert-base-uncased",
                        "thermal_cost": "Low",
                        "downloads": 1000000,
                        "likes": 500,
                        "tags": ["transformers", "pytorch", "bert"],
                        "pipeline_tag": "text-classification",
                        "library_name": "transformers",
                        "description": None,
                    }
                }
            },
        },
        404: {"description": "Model not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_model_details(model_id: str):
    """
    Get detailed information about a specific model

    - **model_id**: The model ID (e.g., bert-base-uncased)
    """
    try:
        # For now, we'll search for the specific model
        # In a real implementation, we'd use HfApi.model_info()
        results = thermal_search(query=model_id, limit=1)

        if not results:
            raise HTTPException(status_code=404, detail=f"Model {model_id} not found")

        model = results[0]

        # Check if this is the exact model we're looking for
        if model["modelId"] != model_id:
            # Try to find exact match
            found = False
            for result in thermal_search(query=model_id, limit=10):
                if result["modelId"] == model_id:
                    model = result
                    found = True
                    break

            if not found:
                raise HTTPException(
                    status_code=404, detail=f"Model {model_id} not found"
                )

        return ModelDetailsResponse(
            modelId=model["modelId"],
            thermal_cost=model.get("thermal_cost", "Unknown"),
            downloads=model.get("downloads", 0),
            likes=model.get("likes", 0),
            tags=model.get("tags", []),
            pipeline_tag=model.get("pipeline_tag"),
            library_name=model.get("library_name"),
            description=None,  # Would need to fetch from model card
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# Root endpoint
@app.get("/")
async def root():
    """API root - redirects to docs"""
    return {"message": "Welcome to Thermal Scout API", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
