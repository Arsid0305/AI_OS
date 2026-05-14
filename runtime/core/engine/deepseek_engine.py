from __future__ import annotations

import logging
import os
import time

from openai import OpenAI
from core.engine.base_engine import BaseEngine

logger = logging.getLogger(__name__)

MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
_BASE_URL = "https://api.deepseek.com"


class DeepSeekEngine(BaseEngine):

    def __init__(self):
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        if not api_key:
            raise RuntimeError("DEEPSEEK_API_KEY не задан. Добавь в .env: DEEPSEEK_API_KEY=...")
        self._client = OpenAI(api_key=api_key, base_url=_BASE_URL)

    def call(self, messages: list[dict], temperature: float = 0.2, **kwargs) -> dict | None:
        start = time.time()
        try:
            logger.debug("[DeepSeek] CALL START model=%s", MODEL)
            response = self._client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=4000,
                timeout=30,
            )
            latency = round(time.time() - start, 2)
            usage = response.usage
            logger.debug("[DeepSeek] DONE: %.2fs", latency)
            return {
                "content": response.choices[0].message.content,
                "latency": latency,
                "tokens_prompt": usage.prompt_tokens if usage else 0,
                "tokens_completion": usage.completion_tokens if usage else 0,
                "model": MODEL,
            }
        except Exception as e:
            logger.error("[DeepSeek] ERROR: %s", e)
            return None
