#!/usr/bin/env python3
"""Test script for API services (IGDB, YouTube, LLM)"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gamecraft_ai.config import settings  # noqa: E402
from src.gamecraft_ai.services.igdb import IGDBService  # noqa: E402
from src.gamecraft_ai.services.llm import LLMService  # noqa: E402
from src.gamecraft_ai.services.youtube import YouTubeService  # noqa: E402


def test_igdb_service():
    """Test IGDB API service"""
    print("🎮 Testing IGDB Service")
    print("=" * 50)

    print(
        f"Client ID: {settings.igdb_client_id[:10]}..."
        if settings.igdb_client_id
        else "❌ No Client ID"
    )
    print(
        f"Access Token: {settings.igdb_access_token[:10]}..."
        if settings.igdb_access_token
        else "❌ No Access Token"
    )

    igdb = IGDBService()

    # Test game search
    print("\n🔍 Searching for 'Zelda Breath of the Wild'...")
    try:
        result = igdb.search_game("Zelda Breath of the Wild")
        if result:
            print(f"✅ Found game: {result['name']}")
            print(f"   Developer: {result['developer']}")
            print(f"   Release Date: {result['release_date']}")
            print(f"   Platforms: {result['platforms']}")
            print(f"   Rating: {result['rating']}")
            return True
        else:
            print("❌ No game data returned")
            return False
    except Exception as e:
        print(f"❌ IGDB Error: {e}")
        return False


def test_youtube_service():
    """Test YouTube API service"""
    print("\n📺 Testing YouTube Service")
    print("=" * 50)

    print(
        f"API Key: {settings.youtube_api_key[:10]}..."
        if settings.youtube_api_key
        else "❌ No API Key"
    )

    youtube = YouTubeService()

    # Test video search
    print("\n🔍 Searching for 'Zelda Breath of the Wild trailer'...")
    try:
        results = youtube.search_videos("Zelda Breath of the Wild trailer", max_results=3)
        if results:
            print(f"✅ Found {len(results)} videos:")
            for i, video in enumerate(results, 1):
                print(f"   {i}. {video['title'][:50]}...")
                print(f"      Channel: {video['channel_name']}")
                print(f"      Video ID: {video['id']}")

            # Test video details
            video_id = results[0]["id"]
            print(f"\n🔍 Getting details for video: {video_id}")
            details = youtube.get_video_details(video_id)
            if details:
                print("✅ Video details retrieved:")
                print(f"   Duration: {details['duration']} seconds")
                print(f"   Views: {details.get('view_count', 'N/A')}")
                return True
            else:
                print("❌ Failed to get video details")
                return False
        else:
            print("❌ No videos found")
            return False
    except Exception as e:
        print(f"❌ YouTube Error: {e}")
        return False


def test_llm_service():
    """Test LLM service"""
    print("\n🤖 Testing LLM Service")
    print("=" * 50)

    print(
        f"OpenAI Key: {settings.openai_api_key[:10]}..."
        if settings.openai_api_key
        else "❌ No OpenAI Key"
    )
    print(
        f"Anthropic Key: {settings.anthropic_api_key[:10]}..."
        if settings.anthropic_api_key
        else "❌ No Anthropic Key"
    )

    llm = LLMService(model="gpt-4o-mini")

    # Test text generation
    print("\n🔍 Testing text generation...")
    try:
        response = llm.generate_text("What is the best Nintendo game?", max_tokens=50)
        if response:
            print(f"✅ LLM Response: {response[:100]}...")
            return True
        else:
            print("❌ No response from LLM")
            return False
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return False


def main():
    """Run all API tests"""
    print("🧪 GameCraft AI - API Services Test")
    print("=" * 60)

    results = {
        "IGDB": test_igdb_service(),
        "YouTube": test_youtube_service(),
        "LLM": test_llm_service(),
    }

    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)

    for service, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{service:10} : {status}")

    total_passed = sum(results.values())
    print(f"\nOverall: {total_passed}/3 services working")

    if total_passed == 3:
        print("🎉 All APIs are working! Ready for full workflow.")
    else:
        print("⚠️  Some APIs need attention before running the full workflow.")
        print("\n💡 Common fixes:")
        print("   • Check API keys in .env file")
        print("   • Verify API quotas and limits")
        print("   • Check network connectivity")


if __name__ == "__main__":
    main()
