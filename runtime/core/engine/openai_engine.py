from __future__ import annotations

import logging
import os
import time

from openai import OpenAI
from core.engine.base_engine import BaseEngine

logger = logging.getLogger(__name__)

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class OpenAIEngine(BaseEngine):

    def __init__(self):
        self._client = OpenAI()

    def call(self, messages: list[dict], temperature: float = 0.2) -> dict | None:
        start = time.time()
        try:
            logger.debug("[OpenAI] CALL START model=%s", MODEL)
            response = self._client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=4000,
                timeout=30,
            )
            latency = round(time.time() - start, 2)
            usage = response.usage
            logger.debug("[OpenAI] DONE: %.2fs", latency)
            return {
                "content": response.choices[0].message.content,
                "latency": latency,
                "tokens_prompt": usage.prompt_tokens if usage else 0,
                "tokens_completion": usage.completion_tokens if usage else 0,
                "model": MODEL,
            }
        except Exception as e:
            logger.error("[OpenAI] ERROR: %s", e)
            return None
