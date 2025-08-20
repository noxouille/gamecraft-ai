from typing import Any

from ..models import EventInfo
from ..services.llm import LLMService
from ..services.youtube import YouTubeService
from ..utils.cache import CacheService


class EventAnalyzerAgent:
    """Event video analysis agent"""

    def __init__(
        self, youtube_service: YouTubeService, llm_service: LLMService, cache_service: CacheService
    ):
        self.youtube = youtube_service
        self.llm = llm_service
        self.cache = cache_service

    def analyze_event(self, state: dict[str, Any]) -> dict[str, Any]:
        """Analyze event video for game announcements"""
        video_url = state["query_metadata"]["video_url"]
        language = state["query"].language

        if not video_url:
            state["errors"].append("No video URL found for event analysis")
            return state

        # Check cache first
        cache_key = f"event_analysis:{video_url}:{language}"
        cached_data = self.cache.get(cache_key)
        if cached_data:
            state.update(cached_data)
            state["cached"] = True
            return state

        # Get video metadata
        video_info = self._get_video_info(video_url)
        if not video_info:
            state["errors"].append("Could not retrieve video information")
            return state

        # Analyze video content (simplified)
        analysis = self._analyze_video_content(video_info, language)

        event_info = EventInfo(
            title=video_info["title"],
            video_url=video_url,
            duration_seconds=video_info.get("duration"),
            announced_games=analysis.get("announced_games", []),
            highlights=analysis.get("highlights", []),
            timestamps=analysis.get("timestamps", {}),
        )

        # Update state
        event_data = {"event_info": event_info}
        state.update(event_data)

        # Cache results
        self.cache.set(cache_key, event_data, ttl=7200)  # 2 hour cache

        return state

    def _get_video_info(self, video_url: str) -> dict[str, Any] | None:
        """Get video metadata from YouTube"""
        try:
            video_id = self._extract_video_id(video_url)
            if not video_id:
                return None

            return self.youtube.get_video_details(video_id)
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None

    def _extract_video_id(self, url: str) -> str | None:
        """Extract video ID from YouTube URL"""
        import re

        patterns = [
            r"youtube\.com/watch\?v=([^&]+)",
            r"youtu\.be/([^?]+)",
            r"youtube\.com/embed/([^?]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def _analyze_video_content(self, video_info: dict[str, Any], language: str) -> dict[str, Any]:
        """Analyze video content for game announcements"""
        try:
            # This is a simplified analysis
            # In a real implementation, you'd use video transcription and NLP

            title = video_info.get("title", "")
            description = video_info.get("description", "")

            # Simple keyword-based analysis
            analysis = {
                "announced_games": self._extract_game_names(title + " " + description),
                "highlights": self._extract_highlights(title, description),
                "timestamps": {},  # Would need video transcription for this
            }

            return analysis
        except Exception as e:
            print(f"Error analyzing video content: {e}")
            return {"announced_games": [], "highlights": [], "timestamps": {}}

    def _extract_game_names(self, text: str) -> list[str]:
        """Extract potential game names from text"""
        import re

        # Simple implementation - would need more sophisticated NER in production
        common_game_patterns = [
            r"Halo \w+",
            r"Call of Duty:? [\w\s]+",
            r"Assassin\'s Creed:? [\w\s]+",
            r"Grand Theft Auto \w+",
            r"The Elder Scrolls:? [\w\s]+",
            r"Final Fantasy [\w\s]+",
        ]

        games = []
        for pattern in common_game_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            games.extend(matches)

        return list(set(games))  # Remove duplicates

    def _extract_highlights(self, title: str, description: str) -> list[str]:
        """Extract key highlights from video"""
        highlights = []

        # Simple keyword-based highlight extraction
        highlight_keywords = [
            "announced",
            "revealed",
            "coming soon",
            "exclusive",
            "first look",
            "gameplay",
            "trailer",
            "release date",
            "beta",
            "early access",
        ]

        text = (title + " " + description).lower()
        for keyword in highlight_keywords:
            if keyword in text:
                # Extract sentence containing the keyword
                sentences = text.split(".")
                for sentence in sentences:
                    if keyword in sentence:
                        highlights.append(sentence.strip().capitalize())
                        break

        return highlights[:5]  # Limit to 5 highlights
