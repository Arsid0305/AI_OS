"""Router — выбирает движок по имени модели.

Поддерживаемые значения --model:
  openai     → OpenAIEngine    (OPENAI_API_KEY)
  anthropic  → AnthropicEngine (ANTHROPIC_API_KEY) — то же что и Claude
  gemini     → GeminiEngine    (GOOGLE_API_KEY)
  deepseek   → DeepSeekEngine  (DEEPSEEK_API_KEY)
"""

from core.engine.base_engine import BaseEngine


def get_engine(model: str) -> BaseEngine:
    model = model.strip().lower()

    if model == "openai":
        from core.engine.openai_engine import OpenAIEngine
        return OpenAIEngine()

    elif model == "anthropic":
        from core.engine.anthropic_engine import AnthropicEngine
        return AnthropicEngine()

    elif model == "gemini":
        from core.engine.gemini_engine import GeminiEngine
        return GeminiEngine()

    elif model == "deepseek":
        from core.engine.deepseek_engine import DeepSeekEngine
        return DeepSeekEngine()

    else:
        raise ValueError(f"Unknown model: '{model}'. Valid: openai, anthropic, gemini, deepseek")
