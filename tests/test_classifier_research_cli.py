#!/usr/bin/env python3
"""CLI test for Classifier and Research Agent integration"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gamecraft_ai.agents.classifier import ClassifierAgent  # noqa: E402
from src.gamecraft_ai.agents.research_agent import ResearchAgent  # noqa: E402
from src.gamecraft_ai.config import settings  # noqa: E402
from src.gamecraft_ai.graph.state import create_initial_state  # noqa: E402
from src.gamecraft_ai.services.igdb import IGDBService  # noqa: E402
from src.gamecraft_ai.services.youtube import YouTubeService  # noqa: E402
from src.gamecraft_ai.utils.cache import CacheService  # noqa: E402


def print_separator(title: str):
    """Print a formatted section separator"""
    print(f"\n{'=' * 60}")
    print(f"🎮 {title}")
    print(f"{'=' * 60}")


def print_result(step: str, success: bool, data: dict | None = None):
    """Print formatted step result"""
    status = "✅ SUCCESS" if success else "❌ FAILED"
    print(f"\n{step}: {status}")
    if data:
        for key, value in data.items():
            print(f"   {key}: {value}")


def print_research_results(result: dict, query_type: str):
    """Print complete research results for Gradio display preview"""
    print_separator("RESEARCH RESULTS FOR GRADIO DISPLAY")

    if query_type == "game":
        # Game Info Tab
        game_info = result.get("game_info")
        if game_info:
            print("📋 GAME INFO TAB:")
            print(f"   Name: {game_info.name}")
            print(f"   Developer: {game_info.developer}")
            print(f"   Publisher: {game_info.publisher}")
            print(f"   Release Date: {game_info.release_date}")
            print(
                f"   Platforms: {', '.join(game_info.platforms) if game_info.platforms else 'N/A'}"
            )
            print(f"   Genre: {game_info.genre}")
            print(
                f"   Description: {game_info.description[:200]}..."
                if game_info.description
                else "   Description: N/A"
            )

        # Media Assets Tab
        media_assets = result.get("media_assets", [])
        print(f"\n🎬 MEDIA ASSETS TAB ({len(media_assets)} items):")
        for i, asset in enumerate(media_assets[:5], 1):  # Show first 5
            print(f"   {i}. {asset.title}")
            print(f"      Type: {asset.asset_type}")
            print(f"      Channel: {asset.channel_name}")
            print(f"      URL: {asset.url}")
            print(f"      Upload Date: {asset.upload_date}")

        # Review Scores Tab
        review_scores = result.get("review_scores", [])
        print(f"\n⭐ REVIEW SCORES TAB ({len(review_scores)} reviews):")
        for score in review_scores:
            print(f"   • {score.outlet_name}: {score.score}/{score.max_score}")
            print(f"     Summary: {score.summary}")
            if score.review_url:
                print(f"     URL: {score.review_url}")

    elif query_type == "event":
        # Event Info Tab
        event_info = result.get("event_info")
        if event_info:
            print("📺 EVENT INFO TAB:")
            print(f"   Name: {event_info.name}")
            print(f"   Description: {event_info.description}")
            print(f"   Video URL: {event_info.video_url}")
            print(f"   Duration: {event_info.duration_seconds}s")
            print(
                f"   Announced Games: {', '.join(event_info.announced_games) if event_info.announced_games else 'None'}"
            )
            print(
                f"   Highlights: {', '.join(event_info.highlights) if event_info.highlights else 'None'}"
            )

        # Media Assets Tab (same format)
        media_assets = result.get("media_assets", [])
        print(f"\n🎬 MEDIA ASSETS TAB ({len(media_assets)} items):")
        for i, asset in enumerate(media_assets[:5], 1):
            print(f"   {i}. {asset.title}")
            print(f"      Type: {asset.asset_type}")
            print(f"      Channel: {asset.channel_name}")
            print(f"      URL: {asset.url}")

    # Processing Info
    processing_time = result.get("processing_time", 0)
    cached = result.get("cached", False)
    print("\n⚙️ PROCESSING INFO:")
    print(f"   Processing Time: {processing_time:.2f}s")
    print(f"   From Cache: {'Yes' if cached else 'No'}")
    print(f"   Total Media Assets: {len(result.get('media_assets', []))}")

    # Errors/Warnings
    errors = result.get("errors", [])
    warnings = result.get("warnings", [])
    if errors:
        print(f"\n❌ ERRORS: {', '.join(errors)}")
    if warnings:
        print(f"\n⚠️ WARNINGS: {', '.join(warnings)}")


def test_classifier_integration(query: str, duration: int = 10):
    """Test classifier agent with real query"""
    print_separator("CLASSIFIER AGENT TEST")

    print(f"📝 Query: {query}")
    print(f"⏱️  Duration: {duration} minutes")

    classifier = ClassifierAgent()

    try:
        # Create proper state format using the real state structure
        state = create_initial_state(query, duration)
        result = classifier.classify_query(dict(state))

        # Check if classification was successful (no errors and query was updated)
        if not result.get("errors") and result.get("query"):
            query_obj = result["query"]
            query_metadata = result.get("query_metadata", {})

            print_result(
                "Classification",
                True,
                {
                    "Type": query_obj.query_type.value
                    if hasattr(query_obj.query_type, "value")
                    else str(query_obj.query_type),
                    "Language": query_obj.language.value
                    if hasattr(query_obj.language, "value")
                    else str(query_obj.language),
                    "Confidence": f"{query_metadata.get('confidence', 0):.2f}",
                    "Game Name": query_metadata.get("game_name", "N/A"),
                    "Event Name": query_metadata.get("event_name", "N/A"),
                    "Script Format": query_metadata.get("script_format", "N/A"),
                },
            )

            # Add success flag for our test logic
            result["success"] = True
            result["is_relevant"] = True  # If we got here, query was relevant
            return result
        else:
            print_result("Classification", False)
            errors = result.get("errors", [])
            if errors:
                print(f"   Errors: {', '.join(errors)}")
            return None

    except Exception as e:
        print_result("Classification", False)
        print(f"   Exception: {e}")
        return None


def test_research_integration(query: str, classification_result: dict):
    """Test research agent with classification result"""
    print_separator("RESEARCH AGENT TEST")

    query_obj = classification_result["query"]
    query_type = (
        query_obj.query_type.value
        if hasattr(query_obj.query_type, "value")
        else str(query_obj.query_type)
    )

    print(f"📝 Query: {query}")
    print(f"🔍 Research Type: {query_type}")

    # Initialize required services
    igdb_service = IGDBService()
    youtube_service = YouTubeService()
    cache_service = CacheService()

    research_agent = ResearchAgent(igdb_service, youtube_service, cache_service)

    try:
        # Use the classification result directly as the state for research
        classification_result["current_step"] = "research"
        result = research_agent.conduct_research(classification_result)

        # Check if research was successful (no errors and research data was added)
        if not result.get("errors") and (
            result.get("game_info") or result.get("event_info") or result.get("media_assets")
        ):
            # Display results based on query type
            if query_type == "game":
                game_info = result.get("game_info")
                media_assets = result.get("media_assets", [])

                print_result(
                    "Game Research",
                    True,
                    {
                        "Game Found": game_info.name if game_info else "N/A",
                        "Developer": game_info.developer if game_info else "N/A",
                        "Release Date": str(game_info.release_date) if game_info else "N/A",
                        "Platforms": str(game_info.platforms) if game_info else "N/A",
                        "Genre": game_info.genre if game_info else "N/A",
                        "Media Assets": len(media_assets),
                        "Video Channels": [
                            v.channel_name for v in media_assets[:3] if v.channel_name
                        ],
                    },
                )

            elif query_type == "event":
                event_info = result.get("event_info")
                media_assets = result.get("media_assets", [])

                print_result(
                    "Event Research",
                    True,
                    {
                        "Event": event_info.name if event_info else "N/A",
                        "Description": (event_info.description[:100] + "...")
                        if event_info and event_info.description
                        else "N/A",
                        "Media Assets": len(media_assets),
                        "Video Sources": [
                            v.metadata.get("channel_name", "Unknown")
                            for v in media_assets[:3]
                            if v.asset_type == "video"
                        ],
                    },
                )

            # Add success flag for our test logic
            result["success"] = True

            # Print detailed results for Gradio preview
            print_research_results(result, query_type)

            return result

        else:
            print_result("Research", False)
            print(f"   Error: {result.get('error', 'Unknown error')}")
            return None

    except Exception as e:
        print_result("Research", False)
        print(f"   Exception: {e}")
        return None


def test_full_integration(query: str, duration: int = 10):
    """Test full classifier -> research agent flow"""
    print_separator("FULL INTEGRATION TEST")
    print("🎯 Testing complete flow: Query → Classification → Research")

    # Step 1: Classify the query
    classification_result = test_classifier_integration(query, duration)

    if not classification_result or not classification_result.get("success"):
        print("\n❌ Integration test failed at classification step")
        return False

    if not classification_result.get("is_relevant"):
        print("\n⚠️  Query classified as not relevant to gaming/YouTube content")
        return False

    # Step 2: Research based on classification
    research_result = test_research_integration(query, classification_result)

    if not research_result or not research_result.get("success"):
        print("\n❌ Integration test failed at research step")
        return False

    # Step 3: Success summary
    print_separator("INTEGRATION TEST SUMMARY")
    print("✅ Classifier Agent: Working")
    print("✅ Research Agent: Working")
    print("✅ API Integration: Working")
    print("✅ End-to-End Flow: SUCCESS")

    return True


def interactive_mode():
    """Interactive mode for testing multiple queries"""
    print_separator("INTERACTIVE TESTING MODE")
    print("Enter queries to test the classifier + research integration")
    print("Type 'quit' to exit")

    while True:
        try:
            query = input("\n🎮 Enter query: ").strip()

            if query.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break

            if not query:
                continue

            # Get duration
            duration_input = input("⏱️  Duration in minutes (default 10): ").strip()
            duration = int(duration_input) if duration_input.isdigit() else 10

            test_full_integration(query, duration)

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Test Classifier and Research Agent Integration")
    parser.add_argument("--query", "-q", help="Single query to test")
    parser.add_argument("--duration", "-d", type=int, default=10, help="Duration in minutes")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--batch", "-b", action="store_true", help="Run batch of predefined tests")

    args = parser.parse_args()

    print("🎮 GameCraft AI - Classifier + Research Agent Integration Test")
    print("=" * 70)

    # Check API status
    print("\n🔧 API Status Check:")
    print(f"   OpenAI: {'✅' if settings.openai_api_key else '❌'}")
    print(f"   IGDB: {'✅' if settings.igdb_client_id and settings.igdb_access_token else '❌'}")
    print(f"   YouTube: {'✅' if settings.youtube_api_key else '❌'}")

    if args.interactive:
        interactive_mode()

    elif args.batch:
        # Predefined test queries
        test_queries = [
            ("Create a review for Zelda Breath of the Wild", 12),
            ("Make a script about Nintendo Direct showcase", 15),
            ("What is the weather today?", 5),  # Should be rejected
            ("Analyze Genshin Impact gameplay mechanics", 10),
            ("Summer Game Fest 2024 highlights", 8),
        ]

        print_separator("BATCH TESTING MODE")
        for i, (query, duration) in enumerate(test_queries, 1):
            print(f"\n🧪 Test {i}/{len(test_queries)}")
            test_full_integration(query, duration)

    elif args.query:
        test_full_integration(args.query, args.duration)

    else:
        print("\nUsage examples:")
        print("  python tests/test_classifier_research_cli.py -q 'Review Zelda BOTW'")
        print("  python tests/test_classifier_research_cli.py --interactive")
        print("  python tests/test_classifier_research_cli.py --batch")


if __name__ == "__main__":
    main()
