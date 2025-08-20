import re
from typing import Any

from ..models import Language, QueryType
from ..services.llm import LLMService


class RelevanceError(Exception):
    """Raised when query is not relevant to gaming or content creation"""

    pass


class ClassifierAgent:
    """Minimal query classification agent"""

    def __init__(self, llm_service: LLMService | None = None, model: str = "gpt-4o-mini"):
        self.llm = llm_service or LLMService(model=model)

    def classify_query(self, state: dict[str, Any]) -> dict[str, Any]:
        """Classify query type and language"""
        query = state["query"]
        query_text = query.text if hasattr(query, "text") else query["text"]

        # First, validate query relevance to gaming and content creation
        relevance_result = self._validate_relevance(query_text)
        if not relevance_result["is_relevant"]:
            raise RelevanceError(relevance_result["message"])

        # Language detection using LLM for better accuracy
        language = self._detect_language_llm(query_text)

        # Query type classification using LLM for better accuracy
        query_type = self._classify_type_llm(query_text)

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
            r"for\s+([^.!?]+?)(?:\s*$|\.|\?|!)",
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

    def _validate_relevance(self, text: str) -> dict[str, Any]:
        """Validate if query is relevant to gaming and YouTube content creation"""
        try:
            prompt = f"""You are a content relevance validator for a gaming YouTube content creation tool.

Analyze this user query and determine if it is relevant to:
1. Video game content (reviews, previews, gameplay, gaming events, game analysis)
2. YouTube content creation (scripts, thumbnails, video production)
3. Gaming industry topics (news, showcases, conferences, releases)

Query: "{text}"

Respond in this exact format:
RELEVANT: [YES/NO]
REASON: [Brief explanation]
CONFIDENCE: [0.0-1.0]

Examples of RELEVANT queries:
- "Create a review script for Zelda Breath of the Wild"
- "Summarize the Nintendo Direct showcase"
- "Make a preview video about Cyberpunk 2077"
- "Generate thumbnail ideas for my gaming channel"

Examples of NOT RELEVANT queries:
- "How to cook pasta"
- "What's the weather today"
- "Write a business plan"
- "Explain quantum physics"""

            response = self.llm.generate_text(prompt, max_tokens=150)
            if not response:
                return {
                    "is_relevant": False,
                    "message": "Unable to validate query relevance. Please try again.",
                }

            # Parse the response
            lines = response.strip().split("\n")
            relevant_line = next((line for line in lines if line.startswith("RELEVANT:")), "")
            reason_line = next((line for line in lines if line.startswith("REASON:")), "")
            confidence_line = next((line for line in lines if line.startswith("CONFIDENCE:")), "")

            is_relevant = "YES" in relevant_line.upper()
            reason = (
                reason_line.replace("REASON:", "").strip()
                if reason_line
                else "Query relevance unclear"
            )

            try:
                confidence = (
                    float(confidence_line.replace("CONFIDENCE:", "").strip())
                    if confidence_line
                    else 0.5
                )
            except ValueError:
                confidence = 0.5

            if not is_relevant:
                return {
                    "is_relevant": False,
                    "message": f"This query is not related to gaming or YouTube content creation. {reason}",
                    "confidence": confidence,
                }

            return {"is_relevant": True, "message": reason, "confidence": confidence}

        except Exception as e:
            print(f"Relevance validation error: {e}")
            # Fallback to simple keyword check if LLM fails
            return self._simple_relevance_check(text)

    def _simple_relevance_check(self, text: str) -> dict[str, Any]:
        """Fallback relevance check using keywords"""
        text_lower = text.lower()

        gaming_keywords = [
            "game",
            "gaming",
            "video game",
            "gameplay",
            "review",
            "preview",
            "trailer",
            "nintendo",
            "playstation",
            "xbox",
            "steam",
            "pc gaming",
            "mobile game",
            "rpg",
            "fps",
            "mmo",
            "indie game",
            "aaa",
            "multiplayer",
            "single player",
            "zelda",
            "mario",
            "pokemon",
            "minecraft",
            "fortnite",
            "call of duty",
            "showcase",
            "direct",
            "conference",
            "e3",
            "gdc",
            "tournament",
            "esports",
        ]

        content_keywords = [
            "youtube",
            "video",
            "script",
            "thumbnail",
            "channel",
            "content creation",
            "streaming",
            "twitch",
            "creator",
            "upload",
            "subscribe",
            "views",
            "monetization",
            "analytics",
            "engagement",
        ]

        gaming_score = sum(1 for keyword in gaming_keywords if keyword in text_lower)
        content_score = sum(1 for keyword in content_keywords if keyword in text_lower)

        total_score = gaming_score + content_score

        if total_score >= 1:  # At least one relevant keyword
            return {
                "is_relevant": True,
                "message": "Query appears gaming/content related",
                "confidence": min(total_score * 0.2, 1.0),
            }

        return {
            "is_relevant": False,
            "message": "This query does not appear to be related to gaming or YouTube content creation.",
            "confidence": 0.1,
        }

    def _detect_language_llm(self, text: str) -> Language:
        """Detect language using LLM with fallback to simple detection"""
        try:
            prompt = f"""Detect the language of this text. Respond with only "ENGLISH" or "FRENCH".

Text: "{text}"

Language:"""

            response = self.llm.generate_text(prompt, max_tokens=10)
            if response and "FRENCH" in response.upper():
                return Language.FRENCH
            elif response and "ENGLISH" in response.upper():
                return Language.ENGLISH
            else:
                # Fallback to simple detection
                return self._detect_language(text)
        except Exception:
            # Fallback to simple detection
            return self._detect_language(text)

    def _classify_type_llm(self, text: str) -> QueryType:
        """Classify query type using LLM with fallback to simple classification"""
        try:
            prompt = f"""Classify this gaming content request into one of two categories:

1. EVENT: Requests about gaming events, showcases, conferences, streams, or analysis of specific videos/URLs
2. GAME: Requests about specific games, game reviews, previews, or general gaming content

Query: "{text}"

Respond with only "EVENT" or "GAME".

Examples:
- "Summarize the Nintendo Direct" → EVENT
- "Create a review of Zelda" → GAME
- "Analyze this YouTube gaming video" → EVENT
- "Write about Cyberpunk 2077" → GAME

Classification:"""

            response = self.llm.generate_text(prompt, max_tokens=10)
            if response and "EVENT" in response.upper():
                return QueryType.EVENT
            elif response and "GAME" in response.upper():
                return QueryType.GAME
            else:
                # Fallback to simple classification
                return self._classify_type(text)
        except Exception:
            # Fallback to simple classification
            return self._classify_type(text)
