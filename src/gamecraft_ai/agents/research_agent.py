"""
Unified Research Agent - handles both game research and event video analysis
"""
import re
from typing import Any

from ..models import EventInfo, GameInfo, MediaAsset, QueryType, ReviewScore
from ..services.igdb import IGDBService
from ..services.youtube import YouTubeService
from ..utils.cache import CacheService


class ResearchAgent:
    """Unified research agent that handles both game info and event video analysis"""

    def __init__(
        self,
        igdb_service: IGDBService,
        youtube_service: YouTubeService,
        cache_service: CacheService,
    ):
        self.igdb = igdb_service
        self.youtube = youtube_service
        self.cache = cache_service

    def conduct_research(self, state: dict[str, Any]) -> dict[str, Any]:
        """Main research method that handles both game and event queries"""
        query = state["query"]
        query_type = query.query_type
        language = query.language

        try:
            if query_type == QueryType.GAME:
                return self._research_game_content(state, language)
            elif query_type == QueryType.EVENT:
                return self._research_event_content(state, language)
            else:
                state["errors"].append("Unknown query type for research")
                return state
        except Exception as e:
            state["errors"].append(f"Research failed: {str(e)}")
            return state

    def _research_game_content(self, state: dict[str, Any], language: str) -> dict[str, Any]:
        """Research content for game queries"""
        game_name = state["query_metadata"].get("game_name")

        if not game_name:
            state["errors"].append("No game name found for research")
            return state

        # Check cache first
        cache_key = f"game_research:{game_name}:{language}"
        cached_data = self.cache.get(cache_key)
        if cached_data:
            state.update(cached_data)
            state["cached"] = True
            return state

        # Gather comprehensive game research
        game_info = self._get_game_info(game_name)
        media_assets = self._get_media_assets(game_name, language)
        review_scores = self._get_review_scores(game_name)

        # Create fallbacks if needed
        if not game_info:
            game_info = self._create_fallback_game_info(game_name)
            state["warnings"].append(f"Using fallback data for game: {game_name}")

        if not review_scores:
            review_scores = self._create_fallback_reviews(game_name)

        # Update state with research results
        research_data = {
            "game_info": game_info,
            "media_assets": media_assets,
            "review_scores": review_scores,
            "research_type": "game",
        }

        state.update(research_data)

        # Cache results for 1 hour
        self.cache.set(cache_key, research_data, ttl=3600)
        return state

    def _research_event_content(self, state: dict[str, Any], language: str) -> dict[str, Any]:
        """Research content for event queries"""
        video_url = state["query_metadata"].get("video_url")

        if not video_url:
            state["errors"].append("No video URL found for event research")
            return state

        # Check cache first
        cache_key = f"event_research:{video_url}:{language}"
        cached_data = self.cache.get(cache_key)
        if cached_data:
            state.update(cached_data)
            state["cached"] = True
            return state

        # Analyze event video
        event_info = self._analyze_event_video(video_url, language)

        if not event_info:
            state["errors"].append("Failed to analyze event video")
            return state

        # Research each announced game
        all_media_assets = []
        all_game_info = []

        for game_name in event_info.announced_games[:5]:  # Limit to top 5 games
            game_info = self._get_game_info(game_name)
            if game_info:
                all_game_info.append(game_info)

            game_media = self._get_media_assets(game_name, language)
            all_media_assets.extend(game_media)

        # Update state with event research results
        research_data = {
            "event_info": event_info,
            "game_info": all_game_info,
            "media_assets": all_media_assets,
            "review_scores": [],  # Events don't typically have review scores
            "research_type": "event",
        }

        state.update(research_data)

        # Cache results for 2 hours
        self.cache.set(cache_key, research_data, ttl=7200)
        return state

    def _get_game_info(self, game_name: str) -> GameInfo | None:
        """Get basic game information from IGDB"""
        try:
            game_data = self.igdb.search_game(game_name)
            if not game_data:
                return None

            return GameInfo(
                name=game_data.get("name", game_name),
                developer=game_data.get("developer"),
                publisher=game_data.get("publisher"),
                release_date=game_data.get("release_date"),
                platforms=game_data.get("platforms", []),
                genre=game_data.get("genre"),
                price=game_data.get("price"),
                description=game_data.get("description"),
            )
        except Exception as e:
            print(f"Error getting game info for {game_name}: {e}")
            return None

    def _get_media_assets(self, game_name: str, language: str) -> list[MediaAsset]:
        """Get media assets from YouTube"""
        try:
            media_assets = []

            # Search for different types of media
            search_queries = [
                f"{game_name} official trailer",
                f"{game_name} gameplay",
                f"{game_name} launch trailer",
                f"{game_name} announcement trailer",
            ]

            for query in search_queries:
                videos = self.youtube.search_videos(query, max_results=2, language=language)
                for video in videos:
                    asset_type = self._determine_asset_type(video["title"], query)
                    media_assets.append(
                        MediaAsset(
                            title=video["title"],
                            url=f"https://www.youtube.com/watch?v={video['id']}",
                            asset_type=asset_type,
                            duration_seconds=video.get("duration"),
                            channel_name=video.get("channel_name"),
                            upload_date=video.get("upload_date"),
                            language=language,
                        )
                    )

            return media_assets
        except Exception as e:
            print(f"Error getting media assets for {game_name}: {e}")
            return []

    def _get_review_scores(self, game_name: str) -> list[ReviewScore]:
        """Get review scores from various sources"""
        try:
            # Mock implementation - in production, integrate with review APIs
            return [
                ReviewScore(
                    outlet_name="IGN",
                    score="85",
                    max_score="100",
                    summary="Solid gameplay with engaging mechanics",
                ),
                ReviewScore(
                    outlet_name="GameSpot",
                    score="8.0",
                    max_score="10",
                    summary="Great experience with minor flaws",
                ),
            ]
        except Exception as e:
            print(f"Error getting review scores for {game_name}: {e}")
            return []

    def _analyze_event_video(self, video_url: str, language: str) -> EventInfo | None:
        """Analyze event video for game announcements"""
        try:
            # Get video metadata
            video_id = self._extract_video_id(video_url)
            if not video_id:
                return None

            video_info = self.youtube.get_video_details(video_id)
            if not video_info:
                return None

            # Extract game announcements from title/description
            title = video_info.get("title", "")
            description = video_info.get("description", "")

            announced_games = self._extract_game_names(title + " " + description)
            highlights = self._extract_highlights(title, description)

            return EventInfo(
                title=title,
                video_url=video_url,
                duration_seconds=video_info.get("duration"),
                announced_games=announced_games,
                highlights=highlights,
                timestamps={},  # Would need video transcription for detailed timestamps
            )

        except Exception as e:
            print(f"Error analyzing event video: {e}")
            return None

    def _extract_video_id(self, url: str) -> str | None:
        """Extract video ID from YouTube URL"""
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

    def _extract_game_names(self, text: str) -> list[str]:
        """Extract potential game names from text"""
        # Simple implementation - would use NER in production
        common_game_patterns = [
            r"Halo \w+",
            r"Call of Duty:? [\w\s]+",
            r"Assassin\'s Creed:? [\w\s]+",
            r"Grand Theft Auto \w+",
            r"The Elder Scrolls:? [\w\s]+",
            r"Final Fantasy [\w\s]+",
            r"Spider-Man [\w\s]*",
            r"Baldur\'s Gate \d+",
            r"Starfield",
            r"Hogwarts Legacy",
        ]

        games = []
        for pattern in common_game_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            games.extend(matches)

        return list(set(games))  # Remove duplicates

    def _extract_highlights(self, title: str, description: str) -> list[str]:
        """Extract key highlights from video"""
        highlights = []
        highlight_keywords = [
            "announced",
            "revealed",
            "coming soon",
            "exclusive",
            "first look",
            "gameplay",
            "trailer",
            "release date",
        ]

        text = (title + " " + description).lower()
        for keyword in highlight_keywords:
            if keyword in text:
                sentences = text.split(".")
                for sentence in sentences:
                    if keyword in sentence and len(sentence.strip()) > 10:
                        highlights.append(sentence.strip().capitalize())
                        break

        return highlights[:5]  # Limit to 5 highlights

    def _determine_asset_type(self, title: str, query: str) -> str:
        """Determine asset type from title and query"""
        title_lower = title.lower()

        if "trailer" in query.lower():
            if "launch" in title_lower or "release" in title_lower:
                return "launch_trailer"
            elif "announce" in title_lower:
                return "announcement_trailer"
            return "trailer"
        elif "gameplay" in query.lower():
            return "gameplay"
        elif "review" in query.lower():
            return "review"

        return "other"

    def _create_fallback_game_info(self, game_name: str) -> GameInfo:
        """Create fallback game info when API fails"""
        return GameInfo(
            name=game_name,
            developer="Game Studio",
            publisher="Publisher",
            release_date="2023",
            platforms=["PC", "PlayStation", "Xbox"],
            genre="Adventure",
            description=f"An exciting {game_name} gaming experience with immersive gameplay and engaging story.",
        )

    def _create_fallback_reviews(self, game_name: str) -> list[ReviewScore]:
        """Create fallback review scores"""
        return [
            ReviewScore(
                outlet_name="Gaming Review",
                score="8.5",
                max_score="10",
                summary="Solid gameplay with engaging mechanics",
            ),
            ReviewScore(
                outlet_name="Game Critic",
                score="85",
                max_score="100",
                summary="Impressive visuals and storytelling",
            ),
        ]
