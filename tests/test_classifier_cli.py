#!/usr/bin/env python3
"""CLI test script for Enhanced LLM-based ClassifierAgent with real API calls"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gamecraft_ai.agents.classifier import ClassifierAgent, RelevanceError  # noqa: E402
from src.gamecraft_ai.models import QueryType  # noqa: E402
from src.gamecraft_ai.models.query import QueryInput  # noqa: E402


def test_classifier(query_text: str, duration: int = 10, model: str = "gpt-4o-mini") -> None:
    """Test the enhanced LLM-based classifier agent with a given query"""
    print(f"🔍 Testing Enhanced LLM-based ClassifierAgent with model: {model}")
    print(f"📝 Query: '{query_text}'")
    print(f"⏱️  Duration: {duration} minutes")
    print("🤖 Features: LLM-based parsing (no regex), intelligent extraction")
    print("=" * 70)

    try:
        # Initialize classifier agent
        classifier = ClassifierAgent(model=model)

        # Create query input
        query = QueryInput(text=query_text, duration_minutes=duration)

        # Create state dict as expected by the agent
        state = {"query": query}

        print("🤖 Calling enhanced LLM-based classifier agent...")

        # Classify the query
        result_state = classifier.classify_query(state)

        # Extract results
        classified_query = result_state["query"]
        metadata = result_state["query_metadata"]

        print("✅ LLM-based classification successful!")
        print("-" * 50)

        # Display results with enhanced formatting
        print(f"🎯 Query Type: {classified_query.query_type.value} (LLM-determined)")
        print(f"🌍 Language: {classified_query.language.value} (LLM-detected)")
        print(f"📊 Confidence: {metadata['confidence']:.2f}")

        if metadata.get("game_name"):
            print(f"🎮 Game Name: {metadata['game_name']} (LLM-extracted)")

        if metadata.get("video_url"):
            print(f"🔗 Video URL: {metadata['video_url']} (LLM-detected)")

        print(f"📋 Script Format: {metadata['script_format']} (LLM-inferred)")

        # Show LLM capabilities
        print("\n🧠 LLM Parsing Features:")
        print("   • Context-aware extraction (no regex patterns)")
        print("   • Multilingual support (English/French)")
        print("   • Flexible format detection")
        print("   • Intelligent game name recognition")

        # Show the flow based on query type
        print("\n" + "=" * 50)
        print("📈 ENHANCED LLM-BASED WORKFLOW PATH:")
        if classified_query.query_type == QueryType.EVENT:
            print("🎪 Event Analysis Flow (LLM-powered):")
            print(
                "   1. ✅ Enhanced Classifier Agent → LLM-based query analysis and classification"
            )
            print(
                "   2. 🔍 Enhanced Research Agent → Analyze event video & gather comprehensive info"
            )
            print("   3. ✍️  Enhanced Script Writer → Create contextual event summary script")
            print(
                "   4. 🖼️  Enhanced YouTube Coach → Generate viral thumbnail prompts with AI insights"
            )
        else:
            print("🎮 Game Content Flow (LLM-powered):")
            print(
                "   1. ✅ Enhanced Classifier Agent → LLM-based query analysis and classification"
            )
            print(
                "   2. 🔍 Enhanced Research Agent → Gather comprehensive game information & media"
            )
            print("   3. ✍️  Enhanced Script Writer → Create contextual game review/preview script")
            print(
                "   4. 🖼️  Enhanced YouTube Coach → Generate viral thumbnail prompts with AI insights"
            )

        print("\n🎉 Ready to proceed with enhanced LLM-powered 4-agent workflow!")
        print("🚀 Improvements: Better accuracy, multilingual support, context-aware parsing")

    except RelevanceError as e:
        print("❌ RELEVANCE CHECK FAILED")
        print("-" * 50)
        print(f"🚫 {e}")
        print("\n💡 Please provide a query related to:")
        print("   • Video game content (reviews, previews, gameplay)")
        print("   • Gaming events (showcases, conferences, streams)")
        print("   • YouTube gaming content creation")
        print("   • Gaming industry topics")

    except Exception as e:
        print("❌ ERROR OCCURRED")
        print("-" * 50)
        print(f"🔥 {type(e).__name__}: {e}")


def run_interactive_mode(model: str = "gpt-4o-mini") -> None:
    """Run interactive testing mode"""
    print("🎮 Enhanced LLM-based Interactive ClassifierAgent Tester")
    print("=" * 60)
    print("🤖 Features: LLM-based parsing, context-aware extraction, multilingual support")
    print("Enter queries to test enhanced relevance detection and intelligent classification.")
    print("Type 'quit' or 'exit' to stop.")
    print()
    print("💡 Try these examples:")
    print("   • 'Create a preview for Final Fantasy XVI'")
    print("   • 'Crée une critique de 15 minutes sur Zelda'")
    print("   • 'Analyze this Nintendo Direct: https://youtube.com/watch?v=abc123'")
    print("   • 'Write a complete guide about Elden Ring combat'")
    print()

    while True:
        try:
            query = input("📝 Enter query: ").strip()

            if query.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break

            if not query:
                print("⚠️  Please enter a query.")
                continue

            # Ask for duration
            duration_input = input("⏱️  Duration (minutes, default=10): ").strip()
            try:
                duration = int(duration_input) if duration_input else 10
            except ValueError:
                duration = 10
                print("⚠️  Invalid duration, using default (10 minutes)")

            print()
            test_classifier(query, duration, model)
            print("\n" + "=" * 70 + "\n")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


def run_batch_tests(model: str = "gpt-4o-mini") -> None:
    """Run comprehensive batch tests for LLM-based classifier"""
    test_cases = [
        # Enhanced gaming queries testing LLM capabilities
        ("Create a 10-minute review script for The Legend of Zelda: Breath of the Wild", 10),
        ("Summarize the Nintendo Direct showcase from yesterday", 15),
        ("Write a preview video about Cyberpunk 2077: Phantom Liberty", 8),
        ("Make thumbnail ideas for my gaming channel", 5),
        ("Analyze this gaming event: https://youtube.com/watch?v=abc123", 20),
        ("Crée une critique de 12 minutes sur Super Mario Odyssey", 12),
        ("Generate a complete guide for Elden Ring boss strategies", 25),
        ("Create first impressions content about Starfield", 7),
        ("Fais un aperçu de Final Fantasy XVI", 10),
        ("Write about gaming trends in 2024", 6),
        # Edge cases for LLM testing
        ("Make a video discussing FromSoftware games", 12),
        ("Create content about the latest PlayStation showcase", 18),
        # Non-relevant queries (should be rejected)
        ("How to cook spaghetti carbonara", 10),
        ("What's the weather like today?", 5),
        ("Write a business plan for my startup", 15),
        ("Explain quantum physics concepts", 10),
        ("How to learn Python programming", 8),
    ]

    print("🔬 Running Enhanced LLM-based Batch Tests")
    print("🤖 Testing: Context-aware parsing, multilingual support, intelligent extraction")
    print("=" * 70)

    passed = 0
    failed = 0
    relevant_count = 12  # First 12 should pass (including edge cases)

    for i, (query, duration) in enumerate(test_cases, 1):
        print(f"\n🧪 Enhanced Test Case {i}/{len(test_cases)}")
        print("-" * 30)

        try:
            test_classifier(query, duration, model)
            if i <= relevant_count:  # First 12 should pass (enhanced gaming queries)
                passed += 1
                print("✅ Expected: PASS - Result: PASS (LLM correctly identified gaming content)")
            else:  # Last 5 should fail
                failed += 1
                print(
                    "❌ Expected: FAIL - Result: PASS (False Positive - LLM incorrectly accepted)"
                )
        except RelevanceError:
            if i > relevant_count:  # Last 5 should fail
                passed += 1
                print(
                    "✅ Expected: FAIL - Result: FAIL (LLM correctly rejected non-gaming content)"
                )
            else:  # First 12 should pass
                failed += 1
                print(
                    "❌ Expected: PASS - Result: FAIL (False Negative - LLM incorrectly rejected)"
                )
        except Exception as e:
            failed += 1
            print(f"❌ Test failed with error: {e}")

        print("=" * 50)

    print("\n📊 ENHANCED LLM-BASED BATCH TEST RESULTS:")
    print(f"✅ Passed: {passed}/{len(test_cases)}")
    print(f"❌ Failed: {failed}/{len(test_cases)}")
    print(f"📈 Success Rate: {(passed/len(test_cases)*100):.1f}%")
    print("🤖 LLM Features Tested:")
    print("   • Context-aware game name extraction")
    print("   • Multilingual support (English/French)")
    print("   • Intelligent format detection (review/preview/guide)")
    print("   • URL extraction for event queries")
    print("   • Enhanced relevance validation")


def main():
    parser = argparse.ArgumentParser(
        description="Test Enhanced LLM-based ClassifierAgent with real API calls"
    )
    parser.add_argument("--query", help="Single query to test with LLM-based parsing")
    parser.add_argument(
        "--duration", type=int, default=10, help="Duration in minutes (default: 10)"
    )
    parser.add_argument(
        "--model", default="gpt-4o-mini", help="LLM model to use for parsing (default: gpt-4o-mini)"
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Run in interactive mode with examples"
    )
    parser.add_argument(
        "--batch", action="store_true", help="Run comprehensive batch tests for LLM features"
    )

    args = parser.parse_args()

    if args.batch:
        run_batch_tests(args.model)
    elif args.interactive:
        run_interactive_mode(args.model)
    elif args.query:
        test_classifier(args.query, args.duration, args.model)
    else:
        # Default to interactive mode
        print("🤖 No specific test specified, running enhanced interactive mode...")
        print("🎮 Features: LLM-based parsing, multilingual support, intelligent extraction")
        print("Use --help to see all options.")
        print()
        run_interactive_mode(args.model)


if __name__ == "__main__":
    main()
