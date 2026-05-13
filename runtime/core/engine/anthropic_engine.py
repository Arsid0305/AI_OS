"""Anthropic Engine — реализует BaseEngine через anthropic SDK.

Установка: pip install anthropic
Переменные окружения:
  ANTHROPIC_API_KEY — ключ API
  ANTHROPIC_MODEL   — например claude-sonnet-4-6 (по умолчанию)
"""

import os
import time

from core.engine.base_engine import BaseEngine

MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")


class AnthropicEngine(BaseEngine):

    def __init__(self):
        try:
            import anthropic
            self._client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        except ImportError:
            raise RuntimeError("anthropic SDK not installed. Run: pip install anthropic")

    def call(self, messages: list[dict], temperature: float = 0.2) -> dict | None:
        import anthropic

        start = time.time()
        try:
            print(">>> [Anthropic] CALL START")

            system_content = ""
            chat_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    system_content += msg["content"] + "\n"
                else:
                    chat_messages.append(msg)

            if not chat_messages:
                raise ValueError("No user/assistant messages — Anthropic requires at least one")

            kwargs = {
                "model": MODEL,
                "max_tokens": 4000,
                "temperature": temperature,
                "messages": chat_messages,
            }
            if system_content.strip():
                kwargs["system"] = system_content.strip()

            response = self._client.messages.create(**kwargs)

            latency = round(time.time() - start, 2)
            content = response.content[0].text if response.content else ""
            usage = response.usage

            print(f">>> [Anthropic] DONE: {latency}s")
            return {
                "content": content,
                "model": MODEL,
                "latency": latency,
                "tokens_prompt": usage.input_tokens if usage else 0,
                "tokens_completion": usage.output_tokens if usage else 0,
            }
        except Exception as e:
            print(f"⛔ [Anthropic] ERROR: {e}")
            return None
