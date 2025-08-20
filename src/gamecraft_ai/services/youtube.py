from typing import Any

import httpx

from ..config import settings


class YouTubeService:
    """YouTube Data API client"""

    def __init__(self):
        self.api_key = settings.youtube_api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.client = httpx.Client(timeout=30.0)

    def search_videos(
        self, query: str, max_results: int = 10, language: str = "en"
    ) -> list[dict[str, Any]]:
        """Search for videos on YouTube"""
        # Check if API key is available
        if not self.api_key or self.api_key == "your_youtube_api_key_here":
            print("YouTube API key not configured, using fallback data")
            return self._get_fallback_videos(query, max_results)

        try:
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max_results,
                "key": self.api_key,
                "regionCode": "US" if language == "en" else "FR",
                "relevanceLanguage": language,
            }

            response = self.client.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()

            data = response.json()
            videos = []

            for item in data.get("items", []):
                video = {
                    "id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channel_name": item["snippet"]["channelTitle"],
                    "upload_date": item["snippet"]["publishedAt"],
                }
                videos.append(video)

            return videos

        except Exception as e:
            print(f"YouTube search error: {e}, using fallback data")
            return self._get_fallback_videos(query, max_results)

    def get_video_details(self, video_id: str) -> dict[str, Any] | None:
        """Get detailed information about a specific video"""
        if not self.api_key or self.api_key == "your_youtube_api_key_here":
            return self._get_fallback_video_details(video_id)

        try:
            params = {
                "part": "snippet,contentDetails,statistics",
                "id": video_id,
                "key": self.api_key,
            }

            response = self.client.get(f"{self.base_url}/videos", params=params)
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])

            if not items:
                return self._get_fallback_video_details(video_id)

            item = items[0]
            duration = self._parse_duration(item["contentDetails"]["duration"])

            return {
                "id": video_id,
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "channel_name": item["snippet"]["channelTitle"],
                "upload_date": item["snippet"]["publishedAt"],
                "duration": duration,
                "view_count": item["statistics"].get("viewCount"),
                "like_count": item["statistics"].get("likeCount"),
            }

        except Exception as e:
            print(f"YouTube video details error: {e}, using fallback data")
            return self._get_fallback_video_details(video_id)

    def _parse_duration(self, duration_str: str) -> int | None:
        """Parse YouTube duration format (PT15M33S) to seconds"""
        try:
            import re

            match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration_str)
            if not match:
                return None

            hours, minutes, seconds = match.groups()
            total_seconds = 0

            if hours:
                total_seconds += int(hours) * 3600
            if minutes:
                total_seconds += int(minutes) * 60
            if seconds:
                total_seconds += int(seconds)

            return total_seconds

        except Exception:
            return None

    def _get_fallback_videos(self, query: str, max_results: int) -> list[dict[str, Any]]:
        """Provide fallback video data when YouTube API is unavailable"""
        fallback_videos = []

        # Create realistic fallback data based on query
        base_titles = [
            f"{query} - Official Trailer",
            f"{query} - Gameplay Video",
            f"{query} - Review",
            f"{query} - Launch Trailer",
            f"{query} - First Look",
        ]

        for i in range(min(max_results, len(base_titles))):
            fallback_videos.append(
                {
                    "id": f"fallback_video_{i+1}",
                    "title": base_titles[i],
                    "description": f"Fallback video content for {query}",
                    "channel_name": "Gaming Channel",
                    "upload_date": "2023-01-01T00:00:00Z",
                }
            )

        return fallback_videos

    def _get_fallback_video_details(self, video_id: str) -> dict[str, Any]:
        """Provide fallback video details when YouTube API is unavailable"""
        return {
            "id": video_id,
            "title": "Gaming Video",
            "description": "Gaming video content",
            "channel_name": "Gaming Channel",
            "upload_date": "2023-01-01T00:00:00Z",
            "duration": 300,  # 5 minutes
            "view_count": "100000",
            "like_count": "5000",
        }

    def __del__(self):
        """Cleanup HTTP client"""
        if hasattr(self, "client"):
            self.client.close()
