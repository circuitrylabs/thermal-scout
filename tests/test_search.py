"""
Tests for thermal_scout.search module
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from thermal_scout.search import estimate_thermal_cost, thermal_search


class TestEstimateThermalCost:
    """Test thermal cost estimation logic"""
    
    def test_tiny_models_return_low_thermal(self):
        """Tiny models should have low thermal cost"""
        model_info = {"modelId": "bert-tiny", "tags": ["tiny"]}
        assert estimate_thermal_cost(model_info) == "Low"
    
    def test_small_models_return_low_thermal(self):
        """Small models should have low thermal cost"""
        model_info = {"modelId": "bert-small", "tags": []}
        assert estimate_thermal_cost(model_info) == "Low"
    
    def test_base_models_return_medium_thermal(self):
        """Base models should have medium thermal cost"""
        model_info = {"modelId": "bert-base-uncased", "tags": []}
        assert estimate_thermal_cost(model_info) == "Medium"
    
    def test_large_models_return_high_thermal(self):
        """Large models should have high thermal cost"""
        model_info = {"modelId": "bert-large", "tags": ["large"]}
        assert estimate_thermal_cost(model_info) == "High"
    
    def test_xl_models_return_high_thermal(self):
        """XL models should have high thermal cost"""
        model_info = {"modelId": "gpt2-xl", "tags": []}
        assert estimate_thermal_cost(model_info) == "High"
    
    def test_distilled_models_reduce_thermal_cost(self):
        """Distilled models should have reduced thermal cost"""
        model_info = {"modelId": "distilbert-base", "tags": ["distilled"]}
        assert estimate_thermal_cost(model_info) == "Low"
    
    def test_parameter_count_affects_thermal(self):
        """Models with parameter counts should be scored appropriately"""
        test_cases = [
            ("model-100m", "Low"),
            ("model-350m", "Low"),
            ("model-1b", "Medium"),
            ("model-7b", "High"),
            ("model-13b", "High"),
        ]
        
        for model_id, expected in test_cases:
            model_info = {"modelId": model_id, "tags": []}
            assert estimate_thermal_cost(model_info) == expected, f"Failed for {model_id}"
    
    def test_efficient_tag_reduces_thermal(self):
        """Efficient tag should reduce thermal cost"""
        model_info = {"modelId": "bert-base", "tags": ["efficient"]}
        # Base would normally be medium, but efficient tag reduces it
        assert estimate_thermal_cost(model_info) == "Low"


class TestThermalSearch:
    """Test thermal search functionality"""
    
    @patch('thermal_scout.search.HfApi')
    def test_basic_search_returns_results(self, mock_hf_api_class, sample_model_list):
        """Basic search should return formatted results"""
        mock_api = Mock()
        mock_hf_api_class.return_value = mock_api
        mock_api.list_models.return_value = sample_model_list
        
        results = thermal_search("bert", limit=3)
        
        assert len(results) == 3
        assert all("modelId" in r for r in results)
        assert all("thermal_cost" in r for r in results)
        mock_api.list_models.assert_called_once()
    
    @patch('thermal_scout.search.HfApi')
    def test_thermal_aware_search_sorts_by_efficiency(self, mock_hf_api_class, sample_model_list):
        """Thermal-aware search should sort by thermal cost"""
        mock_api = Mock()
        mock_hf_api_class.return_value = mock_api
        mock_api.list_models.return_value = sample_model_list
        
        results = thermal_search("bert", limit=3, thermal_aware=True)
        
        # Verify sorting - low thermal cost should come first
        thermal_costs = [r["thermal_cost"] for r in results]
        # Count Low and High thermal costs
        low_count = thermal_costs.count("Low")
        high_count = thermal_costs.count("High")
        # Low thermal models should appear before high thermal models
        assert low_count >= 1
        if high_count > 0:
            # If there are high thermal models, they should be at the end
            assert thermal_costs.index("Low") < thermal_costs.index("High") if "High" in thermal_costs else True
    
    @patch('thermal_scout.search.HfApi')
    def test_non_thermal_aware_preserves_order(self, mock_hf_api_class, sample_model_list):
        """Non-thermal aware search should preserve API order"""
        mock_api = Mock()
        mock_hf_api_class.return_value = mock_api
        mock_api.list_models.return_value = sample_model_list
        
        results = thermal_search("bert", limit=3, thermal_aware=False)
        
        # Should preserve the order from the API (not re-sorted by thermal)
        model_ids = [r["modelId"] for r in results]
        expected_ids = [m.modelId for m in sample_model_list]
        assert model_ids == expected_ids
    
    @patch('thermal_scout.search.HfApi')
    def test_model_type_filter_applied(self, mock_hf_api_class):
        """Model type filter should be passed to API"""
        mock_api = Mock()
        mock_hf_api_class.return_value = mock_api
        mock_api.list_models.return_value = []
        
        thermal_search("bert", model_type="text-generation")
        
        # Verify the API was called with task filter
        call_kwargs = mock_api.list_models.call_args.kwargs
        assert call_kwargs["task"] == "text-generation"
    
    @patch('thermal_scout.search.HfApi')
    def test_empty_results_handled_gracefully(self, mock_hf_api_class):
        """Empty search results should return empty list"""
        mock_api = Mock()
        mock_hf_api_class.return_value = mock_api
        mock_api.list_models.return_value = []
        
        results = thermal_search("nonexistent-model")
        
        assert results == []
    
    @patch('thermal_scout.search.HfApi')
    def test_api_error_handled_gracefully(self, mock_hf_api_class):
        """API errors should be caught and return empty list"""
        mock_api = Mock()
        mock_hf_api_class.return_value = mock_api
        mock_api.list_models.side_effect = Exception("API Error")
        
        results = thermal_search("bert")
        
        assert results == []
    
    @patch('thermal_scout.search.HfApi')
    def test_thermal_search_gets_extra_results_for_filtering(self, mock_hf_api_class):
        """Thermal search should request extra results for better filtering"""
        mock_api = Mock()
        mock_hf_api_class.return_value = mock_api
        mock_api.list_models.return_value = []
        
        thermal_search("bert", limit=10, thermal_aware=True)
        
        # Should request 2x limit for thermal filtering
        call_kwargs = mock_api.list_models.call_args.kwargs
        assert call_kwargs["limit"] == 20
    
    @patch('thermal_scout.search.HfApi')
    def test_model_attributes_preserved(self, mock_hf_api_class, sample_model_list):
        """All model attributes should be preserved in results"""
        mock_api = Mock()
        mock_hf_api_class.return_value = mock_api
        mock_api.list_models.return_value = sample_model_list[:1]
        
        results = thermal_search("bert", limit=1)
        result = results[0]
        
        assert "modelId" in result
        assert "downloads" in result
        assert "likes" in result
        assert "tags" in result
        assert "pipeline_tag" in result
        assert "library_name" in result
        assert "thermal_cost" in result