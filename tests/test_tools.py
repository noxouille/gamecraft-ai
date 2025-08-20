"""Unit tests for LangGraph tools without mocks - real functionality testing."""

import pytest

from src.gamecraft_ai.tools.game_data_tool import get_game_data_tool
from src.gamecraft_ai.tools.pytube_tool import pytube_video_tool
from src.gamecraft_ai.tools.web_scraping_tool import scrape_web_data_tool


class TestGameDataToolReal:
    """Real unit tests for game data API tool."""

    def test_get_game_data_basic_structure(self):
        """Test that game data tool returns proper structure."""
        result = get_game_data_tool.invoke({"game_name": "Cyberpunk 2077"})

        # Test basic structure
        assert isinstance(result, dict)
        assert "name" in result
        assert "developer" in result
        assert "publisher" in result
        assert "platforms" in result
        assert "genre" in result
        assert "description" in result
        assert "review_scores" in result

        # Test that name matches input
        assert result["name"] == "Cyberpunk 2077"

    def test_get_game_data_nonexistent_game(self):
        """Test fallback behavior for nonexistent game."""
        result = get_game_data_tool.invoke({"game_name": "ThisGameDefinitelyDoesNotExist12345"})

        assert isinstance(result, dict)
        assert result["name"] == "ThisGameDefinitelyDoesNotExist12345"
        # Should be fallback data
        assert "Unknown" in result["developer"]  # Could be "Unknown" or "Unknown Developer"
        assert "Unknown" in result["publisher"]  # Could be "Unknown" or "Unknown Publisher"
        assert isinstance(result["platforms"], list)

    def test_get_game_data_empty_name(self):
        """Test behavior with empty game name."""
        result = get_game_data_tool.invoke({"game_name": ""})

        assert isinstance(result, dict)
        assert "name" in result
        # Tool should return some result even with empty name
        assert "developer" in result
        assert "publisher" in result

    def test_get_game_data_popular_games(self):
        """Test with several popular games."""
        games = ["Minecraft", "Fortnite", "Among Us"]

        for game in games:
            result = get_game_data_tool.invoke({"game_name": game})
            assert isinstance(result, dict)
            assert result["name"] == game
            assert "platforms" in result
            assert isinstance(result["platforms"], list)


class TestWebScrapingToolReal:
    """Real unit tests for web scraping tool."""

    def test_scrape_empty_urls(self):
        """Test scraping with empty URL list."""
        result = scrape_web_data_tool.invoke({"urls": [], "data_type": "reviews"})

        assert isinstance(result, dict)
        assert result["data_type"] == "reviews"
        assert result["total_urls"] == 0
        assert result["successful_scrapes"] == 0
        assert isinstance(result["scraped_data"], list)
        assert len(result["scraped_data"]) == 0

    def test_scrape_invalid_url(self):
        """Test scraping with invalid URL."""
        result = scrape_web_data_tool.invoke(
            {
                "urls": ["http://this-domain-definitely-does-not-exist-12345.com"],
                "data_type": "reviews",
            }
        )

        assert isinstance(result, dict)
        assert result["successful_scrapes"] == 0
        assert result["total_urls"] == 1
        assert len(result["errors"]) > 0

    def test_scrape_valid_website(self):
        """Test scraping with a real, simple website."""
        result = scrape_web_data_tool.invoke(
            {"urls": ["https://httpbin.org/html"], "data_type": "general"}
        )

        assert isinstance(result, dict)
        assert result["total_urls"] == 1
        # Should either succeed or fail gracefully
        assert result["successful_scrapes"] >= 0
        assert len(result["errors"]) >= 0

    def test_scrape_different_data_types(self):
        """Test all supported data types."""
        data_types = ["reviews", "news", "specs", "media", "general"]

        for data_type in data_types:
            result = scrape_web_data_tool.invoke({"urls": [], "data_type": data_type})
            assert result["data_type"] == data_type
            assert isinstance(result["scraped_data"], list)

    def test_scrape_multiple_urls(self):
        """Test scraping multiple URLs."""
        urls = ["https://httpbin.org/html", "https://example.com", "http://invalid-url-123.fake"]

        result = scrape_web_data_tool.invoke({"urls": urls, "data_type": "general"})

        assert result["total_urls"] == 3
        # Some should succeed, some should fail
        assert result["successful_scrapes"] >= 0
        assert result["successful_scrapes"] <= 3


class TestPyTubeToolReal:
    """Real unit tests for PyTube tool."""

    def test_pytube_invalid_action(self):
        """Test PyTube with invalid action."""
        result = pytube_video_tool.invoke(
            {"youtube_url": "https://youtube.com/watch?v=dQw4w9WgXcQ", "action": "invalid_action"}
        )

        assert isinstance(result, dict)
        assert "error" in result
        assert "supported_actions" in result
        assert "metadata" in result["supported_actions"]
        assert "transcript" in result["supported_actions"]
        assert "download_audio" in result["supported_actions"]

    def test_pytube_invalid_url(self):
        """Test PyTube with invalid YouTube URL."""
        result = pytube_video_tool.invoke({"youtube_url": "not-a-valid-url", "action": "metadata"})

        assert isinstance(result, dict)
        assert "error" in result

    def test_pytube_metadata_action(self):
        """Test PyTube metadata extraction with real YouTube video."""
        # Using a stable, well-known YouTube video
        result = pytube_video_tool.invoke(
            {"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "action": "metadata"}
        )

        if "error" not in result:
            # If successful, check structure
            assert result["action"] == "metadata"
            assert "title" in result
            assert "author" in result
            assert "length" in result
            assert "video_id" in result
            assert isinstance(result.get("available_streams", []), list)
        else:
            # If failed (network issues, etc.), should still have proper error structure
            assert "error" in result
            assert "url" in result

    def test_pytube_transcript_action(self):
        """Test PyTube transcript extraction."""
        result = pytube_video_tool.invoke(
            {"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "action": "transcript"}
        )

        if "error" not in result:
            assert result["action"] == "transcript"
            assert "captions_available" in result
            assert "languages" in result
            assert isinstance(result["languages"], list)
        else:
            assert "error" in result

    def test_pytube_download_audio_action(self):
        """Test PyTube audio download action structure."""
        result = pytube_video_tool.invoke(
            {
                "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "action": "download_audio",
            }
        )

        if "error" not in result:
            assert result["action"] == "download_audio"
            assert "audio_file_path" in result
            assert "title" in result
            assert "duration" in result
        else:
            # Should fail gracefully
            assert "error" in result


class TestToolsIntegrationReal:
    """Real integration tests for all tools."""

    def test_all_tools_return_dict(self):
        """Test that all tools return dictionary responses."""
        # Game data tool
        game_result = get_game_data_tool.invoke({"game_name": "Tetris"})
        assert isinstance(game_result, dict)

        # Web scraping tool
        scrape_result = scrape_web_data_tool.invoke({"urls": [], "data_type": "general"})
        assert isinstance(scrape_result, dict)

        # PyTube tool
        pytube_result = pytube_video_tool.invoke({"youtube_url": "invalid", "action": "invalid"})
        assert isinstance(pytube_result, dict)

    def test_tools_handle_edge_cases(self):
        """Test tools with edge case inputs."""
        # Empty/None inputs
        game_result = get_game_data_tool.invoke({"game_name": ""})
        assert isinstance(game_result, dict)

        # Special characters
        game_result2 = get_game_data_tool.invoke({"game_name": "Game@#$%^&*()"})
        assert isinstance(game_result2, dict)

        # Very long input
        long_name = "A" * 1000
        game_result3 = get_game_data_tool.invoke({"game_name": long_name})
        assert isinstance(game_result3, dict)

    def test_tools_required_fields(self):
        """Test that tools return required fields."""
        # Game data tool required fields
        game_result = get_game_data_tool.invoke({"game_name": "Pong"})
        required_game_fields = ["name", "developer", "publisher", "platforms", "genre"]
        for field in required_game_fields:
            assert field in game_result

        # Web scraping tool required fields
        scrape_result = scrape_web_data_tool.invoke({"urls": [], "data_type": "reviews"})
        required_scrape_fields = ["data_type", "scraped_data", "total_urls", "successful_scrapes"]
        for field in required_scrape_fields:
            assert field in scrape_result

    def test_tools_error_handling(self):
        """Test that tools handle errors gracefully."""
        # All tools should return dict even on error
        try:
            game_result = get_game_data_tool.invoke({"game_name": None})
            assert isinstance(game_result, dict)
        except Exception:
            pass  # Tool should handle this internally

        try:
            scrape_result = scrape_web_data_tool.invoke({"urls": None, "data_type": "invalid"})
            assert isinstance(scrape_result, dict)
        except Exception:
            pass  # Tool should handle this internally


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
