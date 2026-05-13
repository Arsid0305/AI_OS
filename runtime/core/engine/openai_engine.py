import os
import time
from openai import OpenAI
from core.engine.base_engine import BaseEngine

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class OpenAIEngine(BaseEngine):

    def __init__(self):
        self._client = OpenAI()

    def call(self, messages: list[dict], temperature: float = 0.2) -> dict | None:
        start = time.time()
        try:
            print(">>> [OpenAI] CALL START")
            response = self._client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=4000,
                timeout=30,
            )
            latency = round(time.time() - start, 2)
            usage = response.usage
            print(f">>> [OpenAI] DONE: {latency}s")
            return {
                "content": response.choices[0].message.content,
                "latency": latency,
                "tokens_prompt": usage.prompt_tokens if usage else 0,
                "tokens_completion": usage.completion_tokens if usage else 0,
                "model": MODEL,
            }
        except Exception as e:
            print(f"⛔ [OpenAI] ERROR: {e}")
            return None
