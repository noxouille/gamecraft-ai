from typing import Any

import httpx

from ..config import settings


class LLMService:
    """LLM service client (OpenAI/Anthropic)"""

    # Available models for selection
    AVAILABLE_MODELS = {
        "gpt-4o-mini": {
            "provider": "openai",
            "name": "GPT-4o Mini",
            "description": "Fast, cost-effective model for most tasks",
        },
        "gpt-4o": {
            "provider": "openai",
            "name": "GPT-4o",
            "description": "Most capable OpenAI model",
        },
        "gpt-4-turbo": {
            "provider": "openai",
            "name": "GPT-4 Turbo",
            "description": "Advanced reasoning and longer context",
        },
        "gpt-3.5-turbo": {
            "provider": "openai",
            "name": "GPT-3.5 Turbo",
            "description": "Legacy fast model",
        },
        "claude-3-5-sonnet-20241022": {
            "provider": "anthropic",
            "name": "Claude 3.5 Sonnet",
            "description": "Anthropic's most capable model",
        },
        "claude-3-haiku-20240307": {
            "provider": "anthropic",
            "name": "Claude 3 Haiku",
            "description": "Fast and efficient Anthropic model",
        },
    }

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.openai_api_key = settings.openai_api_key
        self.anthropic_api_key = settings.anthropic_api_key
        self.client = httpx.Client(timeout=60.0)

        # Validate model
        if model not in self.AVAILABLE_MODELS:
            raise ValueError(
                f"Unknown model: {model}. Available models: {list(self.AVAILABLE_MODELS.keys())}"
            )

    @classmethod
    def get_available_models(cls) -> dict[str, dict[str, str]]:
        """Get list of available models for UI selection"""
        return cls.AVAILABLE_MODELS

    def classify_text(self, text: str, categories: list[str]) -> dict[str, Any]:
        """Classify text into categories using LLM"""
        try:
            prompt = f"""
            Classify the following text into one of these categories: {', '.join(categories)}

            Text: {text}

            Respond with just the category name and confidence score (0-1).
            Format: category_name|confidence_score
            """

            response = self._call_llm(prompt, max_tokens=50)
            if response:
                parts = response.strip().split("|")
                if len(parts) == 2:
                    return {"category": parts[0].strip(), "confidence": float(parts[1].strip())}

            return {"category": categories[0], "confidence": 0.5}

        except Exception as e:
            print(f"LLM classification error: {e}")
            return {"category": categories[0], "confidence": 0.5}

    def generate_text(self, prompt: str, max_tokens: int = 1000) -> str | None:
        """Generate text using LLM"""
        try:
            return self._call_llm(prompt, max_tokens)
        except Exception as e:
            print(f"LLM generation error: {e}")
            return None

    def analyze_sentiment(self, text: str) -> dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            prompt = f"""
            Analyze the sentiment of this text and rate it from -1 (very negative) to 1 (very positive).

            Text: {text}

            Respond with just the score: number between -1 and 1
            """

            response = self._call_llm(prompt, max_tokens=10)
            if response:
                try:
                    score = float(response.strip())
                    return {"sentiment_score": max(-1, min(1, score))}
                except ValueError:
                    pass

            return {"sentiment_score": 0.0}

        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {"sentiment_score": 0.0}

    def _call_llm(self, prompt: str, max_tokens: int = 1000) -> str | None:
        """Route to appropriate LLM based on selected model"""
        model_info = self.AVAILABLE_MODELS[self.model]

        if model_info["provider"] == "openai":
            return self._call_openai(prompt, max_tokens)
        elif model_info["provider"] == "anthropic":
            return self._call_anthropic(prompt, max_tokens)
        else:
            raise ValueError(f"Unknown provider: {model_info['provider']}")

    def _call_openai(self, prompt: str, max_tokens: int = 1000) -> str | None:
        """Make API call to OpenAI"""
        if not self.openai_api_key:
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7,
            }

            response = self.client.post(
                "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
            )
            response.raise_for_status()

            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return str(content) if content else None

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None

    def _call_anthropic(self, prompt: str, max_tokens: int = 1000) -> str | None:
        """Make API call to Anthropic (Claude)"""
        if not self.anthropic_api_key:
            return None

        try:
            headers = {
                "x-api-key": self.anthropic_api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
            }

            payload = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            }

            response = self.client.post(
                "https://api.anthropic.com/v1/messages", headers=headers, json=payload
            )
            response.raise_for_status()

            data = response.json()
            content = data["content"][0]["text"]
            return str(content) if content else None

        except Exception as e:
            print(f"Anthropic API error: {e}")
            return None

    def __del__(self):
        """Cleanup HTTP client"""
        if hasattr(self, "client"):
            self.client.close()
