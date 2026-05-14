"""Anthropic Engine — реализует BaseEngine через anthropic SDK."""
from __future__ import annotations
import logging
import os
import time
from core.engine.base_engine import BaseEngine
from core.config import Models

logger = logging.getLogger(__name__)
MODEL   = os.getenv("ANTHROPIC_MODEL", Models.ANTHROPIC_DEFAULT)
_TIMEOUT = 60


class AnthropicEngine(BaseEngine):

    def __init__(self):
        try:
            import anthropic
            self._client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                timeout=_TIMEOUT,
            )
        except ImportError:
            raise RuntimeError("anthropic SDK not installed. Run: pip install anthropic")

    def call(
        self,
        messages: list[dict],
        temperature: float = 0.2,
        model: str | None = None,
        **kwargs,
    ) -> dict | None:
        import anthropic
        _model = model or MODEL
        start  = time.time()
        try:
            logger.debug("[Anthropic] CALL START model=%s", _model)
            system_content = ""
            chat_messages  = []
            for msg in messages:
                if msg["role"] == "system":
                    system_content += msg["content"] + "\n"
                else:
                    chat_messages.append(msg)
            if not chat_messages:
                raise ValueError("No user/assistant messages — Anthropic requires at least one")
            kwargs_api = {
                "model": _model, "max_tokens": 4000,
                "temperature": temperature, "messages": chat_messages,
            }
            if system_content.strip():
                kwargs_api["system"] = system_content.strip()
            response = self._client.messages.create(**kwargs_api)
            latency  = round(time.time() - start, 2)
            content  = response.content[0].text if response.content else ""
            usage    = response.usage
            logger.debug("[Anthropic] DONE: %.2fs", latency)
            return {
                "content": content, "model": _model, "latency": latency,
                "tokens_prompt":     usage.input_tokens if usage else 0,
                "tokens_completion": usage.output_tokens if usage else 0,
            }
        except Exception as e:
            logger.error("[Anthropic] ERROR: %s", e)
            return None
