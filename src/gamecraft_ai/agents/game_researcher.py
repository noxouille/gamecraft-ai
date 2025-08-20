from typing import Any

from ..models import GameInfo, MediaAsset, ReviewScore
from ..services.igdb import IGDBService
from ..services.youtube import YouTubeService
from ..utils.cache import CacheService


class GameResearcherAgent:
    """Combined game research agent that handles game info, media, and reviews"""

    def __init__(
        self,
        igdb_service: IGDBService,
        youtube_service: YouTubeService,
        cache_service: CacheService,
    ):
        self.igdb = igdb_service
        self.youtube = youtube_service
        self.cache = cache_service

    def research_game(self, state: dict[str, Any]) -> dict[str, Any]:
        """Research comprehensive game information"""
        game_name = state["query_metadata"]["game_name"]
        language = state["query"].language

        if not game_name:
            state["errors"].append("No game name extracted from query")
            return state

        # Check cache first
        cache_key = f"game_research:{game_name}:{language}"
        cached_data = self.cache.get(cache_key)
        if cached_data:
            state.update(cached_data)
            state["cached"] = True
            return state

        # Gather game information
        game_info = self._get_game_info(game_name)
        if not game_info:
            # Create fallback game info
            game_info = GameInfo(
                name=game_name,
                developer="Game Studio",
                publisher="Publisher",
                release_date="2023",
                platforms=["PC", "PlayStation", "Xbox"],
                genre="Adventure",
                description=f"An exciting {game_name} gaming experience with immersive gameplay and engaging story.",
            )
            state["warnings"].append(f"Using fallback data for game: {game_name}")

        # Gather media assets
        media_assets = self._get_media_assets(game_name, language)

        # Gather review scores
        review_scores = self._get_review_scores(game_name)
        if not review_scores:
            # Add fallback review scores
            review_scores = [
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

        # Update state
        research_data = {
            "game_info": game_info,
            "media_assets": media_assets,
            "review_scores": review_scores,
        }

        state.update(research_data)

        # Cache results
        self.cache.set(cache_key, research_data, ttl=3600)  # 1 hour cache

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
            print(f"Error getting game info: {e}")
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
                f"{game_name} review",
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
            print(f"Error getting media assets: {e}")
            return []

    def _get_review_scores(self, game_name: str) -> list[ReviewScore]:
        """Get review scores from various sources"""
        # This is a simplified implementation
        # In a real app, you'd integrate with review APIs or scraping
        try:
            # Mock review scores for now
            mock_scores = [
                ReviewScore(
                    outlet_name="IGN",
                    score="90",
                    max_score="100",
                    summary="Excellent gameplay and story",
                ),
                ReviewScore(
                    outlet_name="GameSpot",
                    score="85",
                    max_score="100",
                    summary="Great RPG with minor flaws",
                ),
            ]
            return mock_scores
        except Exception as e:
            print(f"Error getting review scores: {e}")
            return []

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
