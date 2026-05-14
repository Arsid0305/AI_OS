"""BaseEngine — универсальный контракт для всех AI-движков.

Каждый движок ОБЯЗАН реализовать call().
Формат входа: messages (list[dict]) в формате OpenAI chat.
Формат выхода: dict { content, model, latency, tokens_prompt, tokens_completion }
"""
from __future__ import annotations
from abc import ABC, abstractmethod


class BaseEngine(ABC):

    @abstractmethod
    def call(
        self,
        messages: list[dict],
        temperature: float = 0.2,
        **kwargs,
    ) -> dict | None:
        """Send request to model. Returns dict or None on error."""
        raise NotImplementedError
