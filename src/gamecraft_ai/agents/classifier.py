import re
from typing import Any

from ..models import Language, QueryType
from ..services.llm import LLMService


class ClassifierAgent:
    """Minimal query classification agent"""

    def __init__(self, llm_service: LLMService | None = None, model: str = "gpt-4o-mini"):
        self.llm = llm_service or LLMService(model=model)

    def classify_query(self, state: dict[str, Any]) -> dict[str, Any]:
        """Classify query type and language"""
        query = state["query"]
        query_text = query.text if hasattr(query, "text") else query["text"]

        # Simple language detection
        language = self._detect_language(query_text)

        # Simple query type classification
        query_type = self._classify_type(query_text)

        # Extract additional info
        game_name = self._extract_game_name(query_text, query_type)
        video_url = self._extract_video_url(query_text, query_type)
        script_format = self._extract_format(query_text)

        # Create a new QueryInput with updated data
        from ..models import QueryInput

        updated_query = QueryInput(
            text=query_text,
            duration_minutes=query.duration_minutes
            if hasattr(query, "duration_minutes")
            else query.get("duration_minutes", 10),
            query_type=query_type,
            language=language,
        )

        # Add additional attributes as a dict for agents to use
        state["query"] = updated_query
        state["query_metadata"] = {
            "confidence": 0.9,
            "game_name": game_name,
            "video_url": video_url,
            "script_format": script_format,
        }

        return state

    def _detect_language(self, text: str) -> Language:
        """Simple language detection"""
        french_indicators = [
            "fais",
            "crée",
            "résumé",
            "minutes",
            "vidéo",
            "sur",
            "de",
            "une",
            "un",
            "critique",
            "aperçu",
        ]

        text_lower = text.lower()
        french_count = sum(1 for indicator in french_indicators if indicator in text_lower)

        return Language.FRENCH if french_count >= 2 else Language.ENGLISH

    def _classify_type(self, text: str) -> QueryType:
        """Simple query type classification"""
        text_lower = text.lower()

        # Event indicators
        event_patterns = [
            r"showcase",
            r"direct",
            r"event",
            r"conference",
            r"stream",
            r"https?://\S+",
            r"youtube\.com",
            r"youtu\.be",
        ]

        if any(re.search(pattern, text_lower) for pattern in event_patterns):
            return QueryType.EVENT

        return QueryType.GAME

    def _extract_game_name(self, text: str, query_type: QueryType) -> str | None:
        """Extract game name from query"""
        if query_type != QueryType.GAME:
            return None

        # Simple extraction patterns
        patterns = [
            r"about\s+([^.!?]+?)(?:\s*$|\.|\?|!)",
            r"of\s+([^.!?]+?)(?:\s*$|\.|\?|!)",
            r"sur\s+([^.!?]+?)(?:\s*$|\.|\?|!)",
            r"de\s+([^.!?]+?)(?:\s*$|\.|\?|!)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                game_name = match.group(1).strip()
                # Clean up common words
                game_name = re.sub(
                    r"\b(video|review|critique|aperçu)\b", "", game_name, flags=re.IGNORECASE
                )
                return game_name.strip() if game_name.strip() else None

        return None

    def _extract_video_url(self, text: str, query_type: QueryType) -> str | None:
        """Extract video URL from query"""
        if query_type != QueryType.EVENT:
            return None

        # URL extraction
        url_pattern = r"https?://[^\s\]]+|youtube\.com/[^\s\]]+|youtu\.be/[^\s\]]+"
        match = re.search(url_pattern, text)
        return match.group(0) if match else None

    def _extract_format(self, text: str) -> str:
        """Extract script format"""
        text_lower = text.lower()

        # Check for preview first (since "preview" contains "review")
        if any(word in text_lower for word in ["preview", "aperçu", "first impression"]):
            return "preview"
        elif any(word in text_lower for word in ["review", "critique"]):
            return "review"
        elif any(word in text_lower for word in ["summary", "résumé"]):
            return "summary"
        elif any(word in text_lower for word in ["everything", "complete", "guide"]):
            return "complete_guide"

        return "review"  # Default
