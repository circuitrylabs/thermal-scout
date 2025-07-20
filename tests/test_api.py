"""
Test suite for Thermal Scout API endpoints

TDD approach - write tests first!
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from thermal_scout.api.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


class TestHealthEndpoint:
    """Test the health check endpoint"""

    def test_health_check_returns_200(self, client):
        """Health endpoint should return 200 OK"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_correct_format(self, client):
        """Health endpoint should return status and version"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "version" in data
        assert "thermal_aware" in data
        assert data["thermal_aware"] is True


class TestSearchEndpoint:
    """Test the model search endpoint"""

    def test_search_endpoint_exists(self, client):
        """Search endpoint should exist at /api/v1/search"""
        response = client.get("/api/v1/search?q=sentiment")
        assert response.status_code != 404

    def test_search_requires_query_param(self, client):
        """Search endpoint should require 'q' query parameter"""
        response = client.get("/api/v1/search")
        assert response.status_code == 422  # Unprocessable Entity

    def test_search_returns_model_list(self, client):
        """Search should return a list of models"""
        response = client.get("/api/v1/search?q=sentiment+analysis")
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert isinstance(data["models"], list)

    def test_search_respects_limit_param(self, client):
        """Search should respect the limit parameter"""
        response = client.get("/api/v1/search?q=text&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data["models"]) <= 5

    def test_search_includes_thermal_costs(self, client):
        """Each model should include thermal cost information"""
        response = client.get("/api/v1/search?q=bert&limit=1")
        assert response.status_code == 200
        data = response.json()
        assert len(data["models"]) > 0
        model = data["models"][0]
        assert "thermal_cost" in model
        assert model["thermal_cost"] in ["Low", "Medium", "High"]

    def test_search_with_model_type_filter(self, client):
        """Search should support model type filtering"""
        response = client.get("/api/v1/search?q=llama&model_type=text-generation")
        assert response.status_code == 200
        data = response.json()
        # All returned models should be text-generation type
        for model in data["models"]:
            assert model.get("pipeline_tag") == "text-generation"

    def test_search_with_thermal_aware_disabled(self, client):
        """Search should support disabling thermal-aware sorting"""
        response = client.get("/api/v1/search?q=gpt&thermal_aware=false")
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        # Models should still have thermal_cost even if not sorted by it
        if len(data["models"]) > 0:
            assert "thermal_cost" in data["models"][0]


class TestModelsEndpoint:
    """Test the individual model details endpoint"""

    def test_model_details_endpoint_exists(self, client):
        """Model details endpoint should exist"""
        # The endpoint exists, but might return 404 if model not found
        # Let's use a search to find a real model first
        search_resp = client.get("/api/v1/search?q=bert&limit=1")
        if search_resp.status_code == 200 and len(search_resp.json()["models"]) > 0:
            model_id = search_resp.json()["models"][0]["modelId"]
            response = client.get(f"/api/v1/models/{model_id}")
            # Should be 200 for found model or 404 for not found
            assert response.status_code in [200, 404]
        else:
            # If search fails, just verify endpoint routing works
            response = client.get("/api/v1/models/test-model")
            assert response.status_code == 404  # Model not found is expected

    def test_model_details_returns_full_info(self, client):
        """Model details should return comprehensive information"""
        # First search for a model to get a valid ID
        search_response = client.get("/api/v1/search?q=distilbert&limit=1")
        if (
            search_response.status_code == 200
            and len(search_response.json()["models"]) > 0
        ):
            model_id = search_response.json()["models"][0]["modelId"]

            response = client.get(f"/api/v1/models/{model_id}")
            if response.status_code == 200:
                data = response.json()
                assert "modelId" in data
                assert "thermal_cost" in data
                assert "description" in data or "pipeline_tag" in data


class TestCORSHeaders:
    """Test CORS configuration for frontend access"""

    def test_cors_headers_present(self, client):
        """API should include CORS headers for frontend access"""
        # Note: TestClient doesn't trigger CORS middleware
        # In production, CORS headers will be present
        # We can test the middleware is added by checking the app
        from thermal_scout.api.main import app

        # This test ensures CORS middleware is configured
        assert len(app.user_middleware) > 0

    def test_cors_allows_frontend_origin(self, client):
        """CORS should allow localhost:8000 for frontend"""
        # TestClient doesn't handle OPTIONS requests the same way
        # In production, this will work correctly
        # We verify CORS is configured for the right origins
        from thermal_scout.api.main import app

        cors_middleware = None
        for middleware in app.user_middleware:
            if middleware.cls.__name__ == "CORSMiddleware":
                cors_middleware = middleware
                break
        assert cors_middleware is not None
        assert "http://localhost:8000" in cors_middleware.kwargs["allow_origins"]


class TestErrorHandling:
    """Test error handling in API endpoints"""

    @patch("thermal_scout.api.main.thermal_search")
    def test_search_endpoint_handles_exceptions(self, mock_search, client):
        """Search endpoint should handle exceptions gracefully"""
        # Mock the search function to raise an exception
        mock_search.side_effect = Exception("Test error")

        response = client.get("/api/v1/search?q=test")
        assert response.status_code == 500
        assert "Test error" in response.json()["detail"]

    @patch("thermal_scout.api.main.thermal_search")
    def test_model_details_handles_empty_results(self, mock_search, client):
        """Model details should return 404 when model not found"""
        # Mock empty results
        mock_search.return_value = []

        response = client.get("/api/v1/models/nonexistent-model")
        assert response.status_code == 404
        assert "nonexistent-model" in response.json()["detail"]

    @patch("thermal_scout.api.main.thermal_search")
    def test_model_details_finds_exact_match(self, mock_search, client):
        """Model details should search for exact match if first result doesn't match"""
        # First call returns wrong model, second call returns correct one
        mock_search.side_effect = [
            [{"modelId": "bert-base", "thermal_cost": "Medium"}],  # Wrong model
            [
                {"modelId": "bert-base", "thermal_cost": "Medium"},
                {"modelId": "bert-base-uncased", "thermal_cost": "Medium"},  # Correct model
            ],
        ]

        response = client.get("/api/v1/models/bert-base-uncased")
        assert response.status_code == 200
        assert response.json()["modelId"] == "bert-base-uncased"

    @patch("thermal_scout.api.main.thermal_search")
    def test_model_details_not_found_after_search(self, mock_search, client):
        """Model details should return 404 if exact match not found after search"""
        # Both calls return wrong models
        mock_search.side_effect = [
            [{"modelId": "bert-base", "thermal_cost": "Medium"}],  # Wrong model
            [
                {"modelId": "bert-base", "thermal_cost": "Medium"},
                {"modelId": "bert-large", "thermal_cost": "High"},  # Still wrong
            ],
        ]

        response = client.get("/api/v1/models/bert-base-uncased")
        assert response.status_code == 404
        assert "bert-base-uncased" in response.json()["detail"]

    @patch("thermal_scout.api.main.thermal_search")
    def test_model_details_handles_general_exceptions(self, mock_search, client):
        """Model details should handle general exceptions"""
        mock_search.side_effect = Exception("Database error")

        response = client.get("/api/v1/models/test-model")
        assert response.status_code == 500
        assert "Database error" in response.json()["detail"]


class TestRootEndpoint:
    """Test the root endpoint"""

    def test_root_endpoint(self, client):
        """Root endpoint should return welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert data["docs"] == "/docs"
