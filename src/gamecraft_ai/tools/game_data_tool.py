"""Game Data API Tool for IGDB and Steam APIs."""

import logging
from typing import Any

import httpx
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def get_game_data_tool(game_name: str) -> dict[str, Any]:
    """
    Gets comprehensive game data from IGDB and Steam APIs.

    Args:
        game_name: Name of the game to search for

    Returns:
        Dict containing: developer, publisher, release_date, platforms,
        genre, price, review_scores, description, key_features
    """
    try:
        logger.info(f"Fetching game data for: {game_name}")

        # Get data from both APIs
        igdb_data = _fetch_igdb_data(game_name)
        steam_data = _fetch_steam_data(game_name)

        # Merge and return combined data
        combined_data = _merge_game_data(igdb_data, steam_data, game_name)

        logger.info(f"Successfully fetched data for {game_name}")
        return combined_data

    except Exception as e:
        logger.error(f"Error fetching game data for {game_name}: {str(e)}")
        return _get_fallback_data(game_name, str(e))


def _fetch_igdb_data(game_name: str) -> dict[str, Any]:
    """Fetch data from IGDB API."""
    # settings = get_settings()  # TODO: Use when implementing actual IGDB API

    # Mock IGDB API call for now (replace with actual API)
    # TODO: Implement actual IGDB API integration
    mock_data = {
        "name": game_name,
        "developer": "Unknown Developer",
        "publisher": "Unknown Publisher",
        "release_date": "2024-01-01",
        "platforms": ["PC", "PlayStation 5", "Xbox Series X/S"],
        "genre": "Action",
        "description": f"An exciting game called {game_name}",
        "igdb_rating": 85,
        "key_features": ["Single-player", "Multiplayer", "Story-driven"],
    }

    logger.info(f"IGDB data fetched for {game_name}")
    return mock_data


def _fetch_steam_data(game_name: str) -> dict[str, Any]:
    """Fetch data from Steam API."""
    try:
        # Steam Store API search
        search_url = "https://store.steampowered.com/api/storesearch"
        search_params = {"term": game_name, "l": "english", "cc": "US"}

        with httpx.Client(timeout=10.0) as client:
            response = client.get(search_url, params=search_params)
            response.raise_for_status()

            search_data = response.json()

            if search_data.get("items") and len(search_data["items"]) > 0:
                # Get first match
                game = search_data["items"][0]

                # Get detailed info
                app_id = game.get("id")
                if app_id:
                    details = _fetch_steam_app_details(app_id)
                    return {
                        "steam_id": app_id,
                        "steam_name": game.get("name", game_name),
                        "steam_price": game.get("price", "Unknown"),
                        "steam_url": f"https://store.steampowered.com/app/{app_id}",
                        "steam_details": details,
                    }

            return {"steam_found": False}

    except Exception as e:
        logger.warning(f"Steam API error for {game_name}: {str(e)}")
        return {"steam_found": False, "steam_error": str(e)}


def _fetch_steam_app_details(app_id: int) -> dict[str, Any]:
    """Fetch detailed Steam app information."""
    try:
        details_url = "https://store.steampowered.com/api/appdetails"
        params = {"appids": app_id, "l": "english"}

        with httpx.Client(timeout=10.0) as client:
            response = client.get(details_url, params=params)
            response.raise_for_status()

            data = response.json()

            if str(app_id) in data and data[str(app_id)].get("success"):
                game_data = data[str(app_id)]["data"]
                return {
                    "short_description": game_data.get("short_description", ""),
                    "developers": game_data.get("developers", []),
                    "publishers": game_data.get("publishers", []),
                    "release_date": game_data.get("release_date", {}).get("date", ""),
                    "genres": [g.get("description") for g in game_data.get("genres", [])],
                    "categories": [c.get("description") for c in game_data.get("categories", [])],
                    "platforms": game_data.get("platforms", {}),
                    "metacritic": game_data.get("metacritic", {}),
                }

        return {}

    except Exception as e:
        logger.warning(f"Steam app details error for {app_id}: {str(e)}")
        return {}


def _merge_game_data(
    igdb_data: dict[str, Any], steam_data: dict[str, Any], game_name: str
) -> dict[str, Any]:
    """Merge data from IGDB and Steam APIs."""

    # Start with IGDB data as base
    merged = igdb_data.copy()

    # Override/enhance with Steam data where available
    if steam_data.get("steam_found", True):
        steam_details = steam_data.get("steam_details", {})

        # Use Steam data for certain fields if available
        if steam_details.get("developers"):
            merged["developer"] = ", ".join(steam_details["developers"])

        if steam_details.get("publishers"):
            merged["publisher"] = ", ".join(steam_details["publishers"])

        if steam_details.get("release_date"):
            merged["release_date"] = steam_details["release_date"]

        if steam_details.get("short_description"):
            merged["description"] = steam_details["short_description"]

        if steam_details.get("genres"):
            merged["genre"] = ", ".join(steam_details["genres"])

        # Add Steam-specific data
        merged["steam_url"] = steam_data.get("steam_url", "")
        merged["steam_price"] = steam_data.get("steam_price", "Unknown")

        # Add review scores
        merged["review_scores"] = {
            "igdb": merged.get("igdb_rating", 0),
            "metacritic": steam_details.get("metacritic", {}).get("score", 0),
        }

        # Platform information
        steam_platforms = steam_details.get("platforms", {})
        if steam_platforms:
            platforms = []
            if steam_platforms.get("windows"):
                platforms.append("PC")
            if steam_platforms.get("mac"):
                platforms.append("Mac")
            if steam_platforms.get("linux"):
                platforms.append("Linux")
            if platforms:
                merged["platforms"] = platforms

    # Ensure required fields exist
    merged.setdefault("name", game_name)
    merged.setdefault("developer", "Unknown")
    merged.setdefault("publisher", "Unknown")
    merged.setdefault("release_date", "Unknown")
    merged.setdefault("platforms", ["PC"])
    merged.setdefault("genre", "Unknown")
    merged.setdefault("description", f"Game information for {game_name}")
    merged.setdefault("key_features", [])
    merged.setdefault("review_scores", {"igdb": 0, "metacritic": 0})

    return merged


def _get_fallback_data(game_name: str, error: str) -> dict[str, Any]:
    """Return fallback data when API calls fail."""
    return {
        "name": game_name,
        "developer": "Unknown",
        "publisher": "Unknown",
        "release_date": "Unknown",
        "platforms": ["PC"],
        "genre": "Unknown",
        "description": f"Unable to fetch data for {game_name}",
        "key_features": [],
        "review_scores": {"igdb": 0, "metacritic": 0},
        "error": error,
        "data_source": "fallback",
    }
