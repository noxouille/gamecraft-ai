"""
Tests for the LLMService functionality
"""

import sys
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.gamecraft_ai.services.llm import LLMService  # noqa: E402


class TestLLMService:
    """Test cases for LLMService"""

    def test_default_model(self):
        """Test that default model is gpt-4o-mini"""
        service = LLMService()
        assert service.model == "gpt-4o-mini"

    def test_custom_model_selection(self):
        """Test selecting different models"""
        models_to_test = [
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
            "claude-3-5-sonnet-20241022",
            "claude-3-haiku-20240307",
        ]

        for model in models_to_test:
            service = LLMService(model=model)
            assert service.model == model

    def test_invalid_model_raises_error(self):
        """Test that invalid model raises ValueError"""
        with pytest.raises(ValueError, match="Unknown model"):
            LLMService(model="invalid-model")

    def test_available_models_class_method(self):
        """Test that get_available_models returns correct structure"""
        models = LLMService.get_available_models()

        # Should be a dictionary
        assert isinstance(models, dict)

        # Should contain expected models
        expected_models = [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
            "claude-3-5-sonnet-20241022",
            "claude-3-haiku-20240307",
        ]

        for model in expected_models:
            assert model in models
            assert "provider" in models[model]
            assert "name" in models[model]
            assert "description" in models[model]

    def test_model_provider_classification(self):
        """Test that models are correctly classified by provider"""
        models = LLMService.get_available_models()

        openai_models = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]

        anthropic_models = ["claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"]

        for model in openai_models:
            assert models[model]["provider"] == "openai"

        for model in anthropic_models:
            assert models[model]["provider"] == "anthropic"

    def test_service_initialization_with_different_models(self):
        """Test service initialization with different model types"""
        # Test OpenAI models
        openai_service = LLMService(model="gpt-4o")
        assert openai_service.model == "gpt-4o"

        # Test Anthropic models
        anthropic_service = LLMService(model="claude-3-haiku-20240307")
        assert anthropic_service.model == "claude-3-haiku-20240307"

        # Test default
        default_service = LLMService()
        assert default_service.model == "gpt-4o-mini"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
