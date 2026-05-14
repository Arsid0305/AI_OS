"""Startup validation — проверка окружения перед запуском."""
from __future__ import annotations
import os
from core.config import Paths

_MODEL_KEY_MAP: dict[str, str] = {
    "openai":    "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini":    "GOOGLE_API_KEY",
    "deepseek":  "DEEPSEEK_API_KEY",
}

_REQUIRED_DIRS = [
    ("skills_sistem/agents", Paths.SKILLS_DIR),
    ("runtime/prompts",      Paths.PROMPTS_DIR),
    ("MEMORY/tasks",         Paths.MEMORY_TASKS),
    ("MEMORY/lessons",       Paths.MEMORY_LESSONS),
]


def validate(model: str) -> list[str]:
    """Проверить окружение. Возвращает список ошибок. Пустой = всё ок."""
    errors: list[str] = []
    key_name = _MODEL_KEY_MAP.get(model.lower())
    if key_name and not os.getenv(key_name, "").strip():
        errors.append(f"Не задан {key_name} — добавь в .env")
    for label, path in _REQUIRED_DIRS:
        if not path.exists():
            errors.append(f"Директория не найдена: {label}")
    if not Paths.IDENTITY_FILE.exists():
        errors.append("system_identity.json не найден")
    return errors
