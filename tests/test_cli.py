"""
Tests for the CLI interface
"""

import pytest
from typer.testing import CliRunner
from unittest.mock import patch, Mock

from thermal_scout.cli import app

runner = CliRunner()


class TestCLICommands:
    """Test CLI commands"""

    @patch("thermal_scout.cli.thermal_search")
    def test_search_command_basic(self, mock_search):
        """Test basic search command"""
        # Mock search results
        mock_search.return_value = [
            {
                "modelId": "bert-base-uncased",
                "thermal_cost": "Medium",
                "downloads": 1000000,
                "likes": 500,
                "pipeline_tag": "text-classification",
                "tags": ["transformers"],
            }
        ]

        result = runner.invoke(app, ["search", "bert"])
        assert result.exit_code == 0
        assert "bert-base-uncased" in result.stdout
        assert "Medium" in result.stdout

    @patch("thermal_scout.cli.thermal_search")
    def test_search_command_with_limit(self, mock_search):
        """Test search command with limit"""
        mock_search.return_value = []

        result = runner.invoke(app, ["search", "test", "--limit", "5"])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            query="test", limit=5, model_type=None, thermal_aware=True
        )

    @patch("thermal_scout.cli.thermal_search")
    def test_search_command_with_model_type(self, mock_search):
        """Test search command with model type filter"""
        mock_search.return_value = []

        result = runner.invoke(app, ["search", "llama", "--type", "text-generation"])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            query="llama", limit=10, model_type="text-generation", thermal_aware=True
        )

    @patch("thermal_scout.cli.thermal_search")
    def test_search_command_no_thermal(self, mock_search):
        """Test search command with thermal awareness disabled"""
        mock_search.return_value = []

        result = runner.invoke(app, ["search", "gpt", "--no-thermal"])
        assert result.exit_code == 0
        mock_search.assert_called_once_with(
            query="gpt", limit=10, model_type=None, thermal_aware=False
        )

    @patch("thermal_scout.cli.thermal_search")
    def test_search_no_results(self, mock_search):
        """Test search with no results"""
        mock_search.return_value = []

        result = runner.invoke(app, ["search", "nonexistent"])
        assert result.exit_code == 0
        assert "No models found" in result.stdout

    def test_about_command(self):
        """Test about command"""
        result = runner.invoke(app, ["about"])
        assert result.exit_code == 0
        assert "Thermal Scout" in result.stdout
        assert "thermal-aware model search tool" in result.stdout
        assert "Low" in result.stdout
        assert "Medium" in result.stdout
        assert "High" in result.stdout


class TestThermalEmoji:
    """Test thermal emoji conversion"""

    def test_get_thermal_emoji(self):
        """Test thermal cost to emoji conversion"""
        from thermal_scout.cli import get_thermal_emoji

        assert get_thermal_emoji("Low") == "🟢"
        assert get_thermal_emoji("Medium") == "🟡"
        assert get_thermal_emoji("High") == "🔴"
        assert get_thermal_emoji("Unknown") == "⚪"
        assert get_thermal_emoji("Invalid") == "⚪"


class TestCLIEdgeCases:
    """Test edge cases and error handling"""

    @patch("thermal_scout.cli.thermal_search")
    def test_search_with_special_characters(self, mock_search):
        """Test search with special characters in query"""
        mock_search.return_value = []

        result = runner.invoke(app, ["search", "model with spaces & symbols!"])
        assert result.exit_code == 0
        mock_search.assert_called_once()

    @patch("thermal_scout.cli.thermal_search")
    def test_search_with_empty_model_data(self, mock_search):
        """Test handling of incomplete model data"""
        # Mock search with missing fields
        mock_search.return_value = [
            {
                "modelId": "test-model",
                "thermal_cost": "Low",
                # Missing other fields
            }
        ]

        result = runner.invoke(app, ["search", "test"])
        assert result.exit_code == 0
        assert "test-model" in result.stdout
        # Should handle missing fields gracefully