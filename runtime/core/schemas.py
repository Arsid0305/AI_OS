"""Pydantic schemas — типизированные контракты для данных AI_OS.

Защищает от silent crashes при неверной структуре prompt файлов.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, field_validator


class PromptConfig(BaseModel):
    """Контракт для runtime/prompts/<mode>/v1.json."""

    system: str
    user_template: str
    claude_tier: Literal["haiku", "sonnet", "opus"] = "sonnet"

    @field_validator("system")
    @classmethod
    def system_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("system prompt не может быть пустым")
        return v

    @field_validator("user_template")
    @classmethod
    def must_have_input_placeholder(cls, v: str) -> str:
        if "{input}" not in v:
            raise ValueError("user_template должен содержать плейсхолдер {input}")
        return v
