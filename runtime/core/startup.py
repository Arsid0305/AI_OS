"""Startup validation — проверка окружения перед запуском."""
from __future__ import annotations
import json
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

_SKILL_FILES = [
    "SKILL-00_BOOTSTRAP.md",
    "SKILL-01_ANALYZER.md",
    "SKILL-02_VALIDATOR.md",
    "SKILL-03_PLANNER.md",
    "SKILL-04_OPERATOR.md",
    "SKILL-05_WRITER.md",
    "SKILL-06_RESEARCHER.md",
    "SKILL-07_CRITIC.md",
]


def _scan_prompts() -> list[str]:
    """Validate every prompt JSON file in PROMPTS_DIR."""
    errors: list[str] = []
    if not Paths.PROMPTS_DIR.exists():
        return errors
    for subdir in sorted(Paths.PROMPTS_DIR.iterdir()):
        if not subdir.is_dir():
            continue
        v1 = subdir / "v1.json"
        if not v1.exists():
            errors.append(f"Prompt missing: {subdir.name}/v1.json")
            continue
        try:
            raw = json.loads(v1.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in {subdir.name}/v1.json: {e}")
            continue
        if not raw.get("system", "").strip():
            errors.append(f"Empty system prompt: {subdir.name}/v1.json")
        if "{input}" not in raw.get("user_template", ""):
            errors.append(f"Missing {{input}} placeholder: {subdir.name}/v1.json")
    return errors


def _scan_skills() -> list[str]:
    """Check that all expected skill .md files exist."""
    errors: list[str] = []
    if not Paths.SKILLS_DIR.exists():
        return errors
    for filename in _SKILL_FILES:
        if not (Paths.SKILLS_DIR / filename).exists():
            errors.append(f"Skill file missing: skills_sistem/agents/{filename}")
    return errors


def validate(model: str) -> list[str]:
    """Check environment. Returns list of errors — empty list = all ok."""
    errors: list[str] = []
    key_name = _MODEL_KEY_MAP.get(model.lower())
    if key_name and not os.getenv(key_name, "").strip():
        errors.append(f"Не задан {key_name} — добавь в .env")
    for label, path in _REQUIRED_DIRS:
        if not path.exists():
            errors.append(f"Директория не найдена: {label}")
    if not Paths.IDENTITY_FILE.exists():
        errors.append("system_identity.json не найден")
    errors.extend(_scan_prompts())
    errors.extend(_scan_skills())
    return errors
