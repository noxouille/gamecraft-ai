#!/usr/bin/env python3
"""Simple command line test for LLM service"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gamecraft_ai.services.llm import LLMService  # noqa: E402


def test_basic_generation(service: LLMService, prompt: str) -> None:
    """Test basic text generation"""
    print(f"Testing basic generation with model: {service.model}")
    print(f"Prompt: {prompt}")
    print("-" * 50)

    response = service.generate_text(prompt, max_tokens=100)

    if response:
        print(f"Response: {response}")
        print("✅ Test PASSED")
    else:
        print("❌ Test FAILED - No response received")
    print()


def test_classification(service: LLMService) -> None:
    """Test text classification"""
    print("Testing text classification...")

    text = "I love playing Zelda: Breath of the Wild!"
    categories = ["gaming", "cooking", "travel", "technology"]

    print(f"Text: {text}")
    print(f"Categories: {categories}")
    print("-" * 50)

    result = service.classify_text(text, categories)

    print(f"Classification: {result['category']}")
    print(f"Confidence: {result['confidence']}")

    if result["category"] and result["confidence"] > 0:
        print("✅ Test PASSED")
    else:
        print("❌ Test FAILED")
    print()


def test_sentiment(service: LLMService) -> None:
    """Test sentiment analysis"""
    print("Testing sentiment analysis...")

    text = "This game is absolutely amazing! Best purchase ever!"
    print(f"Text: {text}")
    print("-" * 50)

    result = service.analyze_sentiment(text)

    print(f"Sentiment score: {result['sentiment_score']}")

    if -1 <= result["sentiment_score"] <= 1:
        print("✅ Test PASSED")
    else:
        print("❌ Test FAILED")
    print()


def list_models() -> None:
    """List available models"""
    print("Available models:")
    print("-" * 50)

    models = LLMService.get_available_models()
    for model_id, info in models.items():
        print(f"• {model_id}")
        print(f"  Provider: {info['provider']}")
        print(f"  Name: {info['name']}")
        print(f"  Description: {info['description']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Test LLM service functionality")
    parser.add_argument(
        "--model", default="gpt-4o-mini", help="Model to use for testing (default: gpt-4o-mini)"
    )
    parser.add_argument(
        "--prompt",
        default="Hello! Tell me a fun fact about video games.",
        help="Custom prompt to test",
    )
    parser.add_argument("--list-models", action="store_true", help="List available models and exit")
    parser.add_argument(
        "--test",
        choices=["all", "generate", "classify", "sentiment"],
        default="all",
        help="Which test to run (default: all)",
    )

    args = parser.parse_args()

    if args.list_models:
        list_models()
        return

    try:
        # Initialize LLM service
        service = LLMService(model=args.model)
        print(f"Initialized LLM service with model: {args.model}")
        print("=" * 60)
        print()

        # Run tests based on selection
        if args.test in ["all", "generate"]:
            test_basic_generation(service, args.prompt)

        if args.test in ["all", "classify"]:
            test_classification(service)

        if args.test in ["all", "sentiment"]:
            test_sentiment(service)

        print("🎉 All tests completed!")

    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nUse --list-models to see available models")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
