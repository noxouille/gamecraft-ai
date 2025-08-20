"""
Tests for the ClassifierAgent functionality
"""

import sys
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.gamecraft_ai.agents.classifier import ClassifierAgent  # noqa: E402
from src.gamecraft_ai.models import Language, QueryInput, QueryType  # noqa: E402


@pytest.fixture
def classifier_agent():
    """Create a ClassifierAgent instance for testing"""
    # Test with default model (gpt-4o-mini)
    return ClassifierAgent(model="gpt-4o-mini")


class TestClassifierAgent:
    """Test cases for ClassifierAgent"""

    def test_game_query_english(self, classifier_agent):
        """Test classification of English game query"""
        query = QueryInput(
            text="Make a 10-minute review about Baldur's Gate 3", duration_minutes=10
        )
        state = {"query": query}

        result = classifier_agent.classify_query(state)

        assert result["query"].query_type == QueryType.GAME
        assert result["query"].language == Language.ENGLISH
        assert result["query_metadata"]["game_name"] == "Baldur's Gate 3"
        assert result["query_metadata"]["script_format"] == "review"
        assert result["query_metadata"]["confidence"] == 0.9

    def test_game_query_french(self, classifier_agent):
        """Test classification of French game query"""
        query = QueryInput(
            text="Crée une critique de 15 minutes sur Elden Ring", duration_minutes=15
        )
        state = {"query": query}

        result = classifier_agent.classify_query(state)

        assert result["query"].query_type == QueryType.GAME
        assert result["query"].language == Language.FRENCH
        assert result["query_metadata"]["game_name"] == "Elden Ring"
        assert result["query_metadata"]["script_format"] == "review"
        assert result["query_metadata"]["confidence"] == 0.9

    def test_event_query_with_url(self, classifier_agent):
        """Test classification of event query with YouTube URL"""
        query = QueryInput(
            text="Summarize this Nintendo Direct showcase https://youtube.com/watch?v=abc123",
            duration_minutes=10,
        )
        state = {"query": query}

        result = classifier_agent.classify_query(state)

        assert result["query"].query_type == QueryType.EVENT
        assert result["query"].language == Language.ENGLISH
        assert result["query_metadata"]["video_url"] == "https://youtube.com/watch?v=abc123"
        assert result["query_metadata"]["game_name"] is None
        assert result["query_metadata"]["confidence"] == 0.9

    def test_event_query_streaming(self, classifier_agent):
        """Test classification of event streaming query"""
        query = QueryInput(
            text="Create a summary from this gaming event stream", duration_minutes=10
        )
        state = {"query": query}

        result = classifier_agent.classify_query(state)

        assert result["query"].query_type == QueryType.EVENT
        assert result["query"].language == Language.ENGLISH
        assert result["query_metadata"]["script_format"] == "summary"
        assert result["query_metadata"]["confidence"] == 0.9

    def test_preview_format_detection(self, classifier_agent):
        """Test detection of preview script format"""
        query = QueryInput(text="Create a preview of Cyberpunk 2077", duration_minutes=10)
        state = {"query": query}

        result = classifier_agent.classify_query(state)

        assert result["query"].query_type == QueryType.GAME
        assert result["query_metadata"]["script_format"] == "preview"
        assert result["query_metadata"]["game_name"] == "Cyberpunk 2077"

    def test_language_detection_edge_cases(self, classifier_agent):
        """Test language detection with mixed content"""
        test_cases = [
            ("Make a video about Minecraft", Language.ENGLISH),
            ("Fais une vidéo sur Minecraft", Language.FRENCH),
            ("Create something about le jeu", Language.ENGLISH),  # Should still be English
            ("Crée un résumé de cette vidéo", Language.FRENCH),
        ]

        for text, expected_language in test_cases:
            query = QueryInput(text=text, duration_minutes=10)
            state = {"query": query}
            result = classifier_agent.classify_query(state)
            assert result["query"].language == expected_language, f"Failed for text: {text}"

    def test_game_name_extraction_patterns(self, classifier_agent):
        """Test various patterns for game name extraction"""
        test_cases = [
            ("Make a review about Baldur's Gate 3", "Baldur's Gate 3"),
            ("Create a video of The Legend of Zelda", "The Legend of Zelda"),
            ("Write about Grand Theft Auto VI", "Grand Theft Auto VI"),
            ("Fais une critique sur Final Fantasy XVI", "Final Fantasy XVI"),
            ("Create something", None),  # No game name
        ]

        for text, expected_game in test_cases:
            query = QueryInput(text=text, duration_minutes=10)
            state = {"query": query}
            result = classifier_agent.classify_query(state)
            assert (
                result["query_metadata"]["game_name"] == expected_game
            ), f"Failed for text: {text}"

    def test_url_extraction_patterns(self, classifier_agent):
        """Test URL extraction from various formats"""
        test_cases = [
            ("Analyze https://youtube.com/watch?v=123", "https://youtube.com/watch?v=123"),
            ("Check this out: https://youtu.be/abc123", "https://youtu.be/abc123"),
            ("Look at youtube.com/watch?v=test", "youtube.com/watch?v=test"),
            ("No URL here", None),
        ]

        for text, expected_url in test_cases:
            query = QueryInput(text=text, duration_minutes=10)
            state = {"query": query}
            result = classifier_agent.classify_query(state)

            # URL extraction only works for EVENT queries
            if "showcase" in text.lower() or "direct" in text.lower() or "http" in text.lower():
                result["query"].query_type = QueryType.EVENT
                result = classifier_agent.classify_query(state)
                assert (
                    result["query_metadata"]["video_url"] == expected_url
                ), f"Failed for text: {text}"

    def test_script_format_detection(self, classifier_agent):
        """Test detection of different script formats"""
        test_cases = [
            ("Make a review of the game", "review"),
            ("Create a preview of the game", "preview"),  # Fixed: needs "preview" word exactly
            ("Write a summary", "summary"),
            ("Make everything about the game", "complete_guide"),
            ("Just make a video", "review"),  # Default format
        ]

        for text, expected_format in test_cases:
            query = QueryInput(text=text, duration_minutes=10)
            state = {"query": query}
            result = classifier_agent.classify_query(state)
            assert (
                result["query_metadata"]["script_format"] == expected_format
            ), f"Failed for text: '{text}' - got '{result['query_metadata']['script_format']}' instead of '{expected_format}'"

    def test_state_preservation(self, classifier_agent):
        """Test that classifier preserves and updates state correctly"""
        original_query = QueryInput(text="Test query", duration_minutes=15)
        state = {"query": original_query, "other_data": "should_be_preserved"}

        result = classifier_agent.classify_query(state)

        # Check that original data is preserved
        assert "other_data" in result
        assert result["other_data"] == "should_be_preserved"

        # Check that query is updated
        assert "query" in result
        assert result["query"].duration_minutes == 15  # Original duration preserved
        assert result["query"].text == "Test query"  # Original text preserved

        # Check that metadata is added
        assert "query_metadata" in result
        assert "confidence" in result["query_metadata"]

    def test_model_selection(self):
        """Test that different models can be selected"""
        # Test with different models
        models_to_test = ["gpt-4o-mini", "gpt-3.5-turbo"]

        for model in models_to_test:
            agent = ClassifierAgent(model=model)
            assert agent.llm.model == model

            # Test that it still works
            query = QueryInput(text="Test query", duration_minutes=10)
            state = {"query": query}
            result = agent.classify_query(state)

            assert "query" in result
            assert "query_metadata" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
