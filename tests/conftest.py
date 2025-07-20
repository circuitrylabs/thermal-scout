"""
Shared pytest fixtures and configuration for thermal-scout tests
"""

from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_hf_api(monkeypatch):
    """Mock HuggingFace Hub API"""
    mock_api = Mock()
    monkeypatch.setattr("huggingface_hub.HfApi", lambda: mock_api)
    return mock_api


@pytest.fixture
def sample_model_info():
    """Sample model information for testing"""
    return {
        "modelId": "distilbert-base-uncased",
        "downloads": 1000000,
        "likes": 500,
        "tags": ["transformers", "pytorch", "bert", "distilled"],
        "pipeline_tag": "text-classification",
        "library_name": "transformers",
        "siblings": [
            {"rfilename": "pytorch_model.bin", "size": 250_000_000},
            {"rfilename": "config.json", "size": 1000},
        ],
    }


@pytest.fixture
def sample_model_list():
    """Sample list of models for search results"""
    return [
        Mock(
            modelId="bert-tiny",
            downloads=500000,
            likes=200,
            tags=["transformers", "pytorch", "tiny"],
            pipeline_tag="text-classification",
            library_name="transformers",
        ),
        Mock(
            modelId="bert-large-uncased",
            downloads=2000000,
            likes=1000,
            tags=["transformers", "pytorch", "bert", "large"],
            pipeline_tag="fill-mask",
            library_name="transformers",
        ),
        Mock(
            modelId="distilbert-base-uncased",
            downloads=1000000,
            likes=500,
            tags=["transformers", "pytorch", "bert", "distilled"],
            pipeline_tag="text-classification",
            library_name="transformers",
        ),
    ]


@pytest.fixture
def mock_cache_info():
    """Mock cache information"""
    mock_info = Mock()
    mock_info.size_on_disk = 1_000_000_000  # 1GB
    mock_info.cache_dir = "/home/user/.cache/huggingface"
    mock_info.repos = [
        Mock(repo_id="bert-base-uncased", size_on_disk=500_000_000),
        Mock(repo_id="gpt2", size_on_disk=500_000_000),
    ]
    mock_info.warnings = []
    return mock_info
