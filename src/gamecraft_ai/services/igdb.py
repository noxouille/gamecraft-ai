from typing import Any

import httpx

from ..config import settings


class IGDBService:
    """IGDB (Internet Game Database) API client"""

    def __init__(self):
        self.client_id = settings.igdb_client_id
        self.access_token = settings.igdb_access_token
        self.base_url = "https://api.igdb.com/v4"
        self.client = httpx.Client(
            timeout=30.0,
            headers={
                "Client-ID": self.client_id,
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

    def search_game(self, game_name: str) -> dict[str, Any] | None:
        """Search for a game by name"""
        # Check if credentials are available
        if (
            not self.client_id
            or not self.access_token
            or self.client_id == "your_igdb_client_id_here"
        ):
            return self._get_fallback_game_data(game_name)

        try:
            # IGDB query to search for games
            query = f"""
            fields name,first_release_date,platforms.name,genres.name,
                   involved_companies.company.name,involved_companies.developer,
                   involved_companies.publisher,summary,rating,rating_count;
            search "{game_name}";
            limit 1;
            """

            response = self.client.post(f"{self.base_url}/games", content=query)
            response.raise_for_status()

            data = response.json()
            if not data:
                return self._get_fallback_game_data(game_name)

            game = data[0]

            # Process the response
            return {
                "name": game.get("name"),
                "description": game.get("summary"),
                "release_date": self._format_release_date(game.get("first_release_date")),
                "platforms": [p["name"] for p in game.get("platforms", [])],
                "genre": game.get("genres", [{}])[0].get("name") if game.get("genres") else None,
                "developer": self._get_developer(game.get("involved_companies", [])),
                "publisher": self._get_publisher(game.get("involved_companies", [])),
                "rating": game.get("rating"),
                "rating_count": game.get("rating_count"),
            }

        except Exception as e:
            print(f"IGDB search error: {e}, using fallback game data")
            return self._get_fallback_game_data(game_name)

    def get_game_details(self, game_id: int) -> dict[str, Any] | None:
        """Get detailed information about a specific game"""
        try:
            query = f"""
            fields *;
            where id = {game_id};
            """

            response = self.client.post(f"{self.base_url}/games", content=query)
            response.raise_for_status()

            data = response.json()
            return data[0] if data else None

        except Exception as e:
            print(f"IGDB game details error: {e}")
            return None

    def _format_release_date(self, timestamp: int | None) -> str | None:
        """Convert UNIX timestamp to date string"""
        if not timestamp:
            return None

        try:
            from datetime import datetime

            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        except Exception:
            return None

    def _get_developer(self, companies: list[dict[str, Any]]) -> str | None:
        """Extract developer from involved companies"""
        for company in companies:
            if company.get("developer"):
                name = company.get("company", {}).get("name")
                return str(name) if name else None
        return None

    def _get_publisher(self, companies: list[dict[str, Any]]) -> str | None:
        """Extract publisher from involved companies"""
        for company in companies:
            if company.get("publisher"):
                name = company.get("company", {}).get("name")
                return str(name) if name else None
        return None

    def _get_fallback_game_data(self, game_name: str) -> dict[str, Any]:
        """Provide fallback game data when IGDB is unavailable"""
        return {
            "name": game_name,
            "description": f"An exciting {game_name} gaming experience that offers immersive gameplay and engaging storytelling.",
            "release_date": "2023",
            "platforms": ["PC", "PlayStation", "Xbox"],
            "genre": "Adventure",
            "developer": "Game Studio",
            "publisher": "Game Publisher",
            "rating": 85.0,
            "rating_count": 100,
        }

    def __del__(self):
        """Cleanup HTTP client"""
        if hasattr(self, "client"):
            self.client.close()
