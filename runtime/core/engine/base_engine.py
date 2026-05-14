"""BaseEngine — универсальный контракт для всех AI-движков.

Каждый движок ОБЯЗАН реализовать метод call().
Формат входа: messages (list[dict]) в формате OpenAI/Anthropic chat.
Формат выхода: dict с полями:
  - content: str
  - model: str
  - latency: float (секунды)
  - tokens_prompt: int
  - tokens_completion: int
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseEngine(ABC):

    @abstractmethod
    def call(self, messages: list[dict], temperature: float = 0.2) -> dict | None:
        """
        Отправить запрос к модели.

        messages: [{"role": "system"|"user"|"assistant", "content": "..."}]
        temperature: 0.0–1.0

        Возвращает dict или None при ошибке.
        """
        raise NotImplementedError
