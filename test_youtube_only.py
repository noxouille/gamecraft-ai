#!/usr/bin/env python3
"""Quick test for YouTube API only"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.gamecraft_ai.config import settings  # noqa: E402
from src.gamecraft_ai.services.youtube import YouTubeService  # noqa: E402


def test_youtube():
    print("📺 Testing YouTube API")
    print(f"API Key: {settings.youtube_api_key[:15]}...")

    youtube = YouTubeService()

    try:
        # Test a simple search
        results = youtube.search_videos("Nintendo Direct", max_results=1)
        if results and not results[0]["id"].startswith("fallback"):
            print("✅ YouTube API working!")
            print(f"Found: {results[0]['title']}")
            return True
        else:
            print("❌ Still using fallback data - API not enabled")
            return False
    except Exception as e:
        print(f"❌ YouTube Error: {e}")
        return False


if __name__ == "__main__":
    test_youtube()
