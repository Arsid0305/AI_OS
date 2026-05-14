"""Router — выбирает движок по имени модели.

Поддерживаемые значения --model:
  openai     → OpenAIEngine   (использует OPENAI_API_KEY)
  anthropic  → AnthropicEngine (использует ANTHROPIC_API_KEY)
  claude     → AnthropicEngine (алиас)
  gemini     → GeminiEngine    (использует GOOGLE_API_KEY)
"""

from core.engine.base_engine import BaseEngine


def get_engine(model: str) -> BaseEngine:
    model = model.strip().lower()

    if model == "openai":
        from core.engine.openai_engine import OpenAIEngine
        return OpenAIEngine()

    elif model in ("anthropic", "claude"):
        from core.engine.anthropic_engine import AnthropicEngine
        return AnthropicEngine()

    elif model == "gemini":
        from core.engine.gemini_engine import GeminiEngine
        return GeminiEngine()

    else:
        raise ValueError(f"Unknown model: '{model}'. Valid: openai, anthropic, claude, gemini")
