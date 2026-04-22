"""Router — выбирает движок по имени модели.

Поддерживаемые значения --model:
  openai     → OpenAIEngine (gpt-4o-mini по умолчанию)
  anthropic  → AnthropicEngine (claude-sonnet-4 по умолчанию)
  claude     → AnthropicEngine (алиас)
  gemini     → не реализован (NotImplementedError)
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
        raise NotImplementedError("Gemini engine not implemented yet")

    else:
        raise ValueError(f"Unknown model: '{model}'. Valid: openai, anthropic, claude, gemini")
