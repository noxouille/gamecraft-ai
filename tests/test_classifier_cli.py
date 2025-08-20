#!/usr/bin/env python3
"""CLI test script for ClassifierAgent with real API calls"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gamecraft_ai.agents.classifier import ClassifierAgent, RelevanceError  # noqa: E402
from src.gamecraft_ai.models import QueryType  # noqa: E402
from src.gamecraft_ai.models.query import QueryInput  # noqa: E402


def test_classifier(query_text: str, duration: int = 10, model: str = "gpt-4o-mini") -> None:
    """Test the classifier agent with a given query"""
    print(f"🔍 Testing ClassifierAgent with model: {model}")
    print(f"📝 Query: '{query_text}'")
    print(f"⏱️  Duration: {duration} minutes")
    print("=" * 70)

    try:
        # Initialize classifier agent
        classifier = ClassifierAgent(model=model)

        # Create query input
        query = QueryInput(text=query_text, duration_minutes=duration)

        # Create state dict as expected by the agent
        state = {"query": query}

        print("🤖 Calling classifier agent...")

        # Classify the query
        result_state = classifier.classify_query(state)

        # Extract results
        classified_query = result_state["query"]
        metadata = result_state["query_metadata"]

        print("✅ Classification successful!")
        print("-" * 50)

        # Display results
        print(f"🎯 Query Type: {classified_query.query_type.value}")
        print(f"🌍 Language: {classified_query.language.value}")
        print(f"📊 Confidence: {metadata['confidence']:.2f}")

        if metadata.get("game_name"):
            print(f"🎮 Game Name: {metadata['game_name']}")

        if metadata.get("video_url"):
            print(f"🔗 Video URL: {metadata['video_url']}")

        print(f"📋 Script Format: {metadata['script_format']}")

        # Show the flow based on query type
        print("\n" + "=" * 50)
        print("📈 COMPLETE WORKFLOW PATH:")
        if classified_query.query_type == QueryType.EVENT:
            print("🎪 Event Analysis Flow:")
            print("   1. ✅ Classifier Agent → Query validated and classified")
            print("   2. 🔍 Research Agent → Analyze event video & gather info")
            print("   3. ✍️  Script Writer → Create event summary script")
            print("   4. 🖼️  YouTube Coach → Generate viral thumbnail prompts")
        else:
            print("🎮 Game Content Flow:")
            print("   1. ✅ Classifier Agent → Query validated and classified")
            print("   2. 🔍 Research Agent → Gather game information & media")
            print("   3. ✍️  Script Writer → Create game review/preview script")
            print("   4. 🖼️  YouTube Coach → Generate viral thumbnail prompts")

        print("\n🎉 Ready to proceed with complete 4-agent workflow!")

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
    print("🎮 Interactive ClassifierAgent Tester")
    print("=" * 50)
    print("Enter queries to test relevance and classification.")
    print("Type 'quit' or 'exit' to stop.")
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
    """Run predefined batch tests"""
    test_cases = [
        # Relevant gaming queries
        ("Create a 10-minute review script for Zelda: Breath of the Wild", 10),
        ("Summarize the Nintendo Direct showcase from yesterday", 15),
        ("Write a preview video about Cyberpunk 2077", 8),
        ("Make thumbnail ideas for my gaming channel", 5),
        ("Analyze this gaming event: https://youtube.com/watch?v=abc123", 20),
        ("Crée une critique de 12 minutes sur Mario Odyssey", 12),
        # Non-relevant queries (should be rejected)
        ("How to cook spaghetti carbonara", 10),
        ("What's the weather like today?", 5),
        ("Write a business plan for my startup", 15),
        ("Explain quantum physics concepts", 10),
        ("How to learn Python programming", 8),
    ]

    print("🔬 Running Batch Tests")
    print("=" * 70)

    passed = 0
    failed = 0

    for i, (query, duration) in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}/{len(test_cases)}")
        print("-" * 30)

        try:
            test_classifier(query, duration, model)
            if i <= 6:  # First 6 should pass
                passed += 1
                print("✅ Expected: PASS - Result: PASS")
            else:  # Last 5 should fail
                failed += 1
                print("❌ Expected: FAIL - Result: PASS (False Positive)")
        except RelevanceError:
            if i > 6:  # Last 5 should fail
                passed += 1
                print("✅ Expected: FAIL - Result: FAIL")
            else:  # First 6 should pass
                failed += 1
                print("❌ Expected: PASS - Result: FAIL (False Negative)")
        except Exception as e:
            failed += 1
            print(f"❌ Test failed with error: {e}")

        print("=" * 50)

    print("\n📊 BATCH TEST RESULTS:")
    print(f"✅ Passed: {passed}/{len(test_cases)}")
    print(f"❌ Failed: {failed}/{len(test_cases)}")
    print(f"📈 Success Rate: {(passed/len(test_cases)*100):.1f}%")


def main():
    parser = argparse.ArgumentParser(description="Test ClassifierAgent with real API calls")
    parser.add_argument("--query", help="Single query to test")
    parser.add_argument(
        "--duration", type=int, default=10, help="Duration in minutes (default: 10)"
    )
    parser.add_argument(
        "--model", default="gpt-4o-mini", help="LLM model to use (default: gpt-4o-mini)"
    )
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--batch", action="store_true", help="Run predefined batch tests")

    args = parser.parse_args()

    if args.batch:
        run_batch_tests(args.model)
    elif args.interactive:
        run_interactive_mode(args.model)
    elif args.query:
        test_classifier(args.query, args.duration, args.model)
    else:
        # Default to interactive mode
        print("No specific test specified, running interactive mode...")
        print("Use --help to see all options.")
        print()
        run_interactive_mode(args.model)


if __name__ == "__main__":
    main()
