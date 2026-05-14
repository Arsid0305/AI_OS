import os
import time
from openai import OpenAI
from core.engine.base_engine import BaseEngine

# Gemini через OpenAI-совместимый API Google
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


class GeminiEngine(BaseEngine):

    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            raise RuntimeError("⛔ GOOGLE_API_KEY не задан. Добавь в .env: GOOGLE_API_KEY=...")
        self._client = OpenAI(api_key=api_key, base_url=_BASE_URL)

    def call(self, messages: list[dict], temperature: float = 0.2, **kwargs) -> dict | None:
        start = time.time()
        try:
            print(f">>> [Gemini] CALL START ({MODEL})")
            response = self._client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=4000,
                timeout=30,
            )
            latency = round(time.time() - start, 2)
            usage = response.usage
            print(f">>> [Gemini] DONE: {latency}s")
            return {
                "content": response.choices[0].message.content,
                "latency": latency,
                "tokens_prompt": usage.prompt_tokens if usage else 0,
                "tokens_completion": usage.completion_tokens if usage else 0,
                "model": MODEL,
            }
        except Exception as e:
            print(f"⛔ [Gemini] ERROR: {e}")
            return None
