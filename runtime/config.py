"""Central config — все пути и константы в одном месте.

Импортируй: from config import Paths, Models, APP_VERSION
"""

from __future__ import annotations

from pathlib import Path

# Корень репозитория
_ROOT = Path(__file__).resolve().parents[1]
_RUNTIME = Path(__file__).resolve().parent


class Paths:
    """All filesystem paths. Absolute, calculated once."""

    # Корневые
    ROOT         = _ROOT
    RUNTIME      = _RUNTIME

    # Skills
    SKILLS_DIR   = _ROOT / "skills_sistem" / "agents"

    # Prompts
    PROMPTS_DIR  = _RUNTIME / "prompts"

    # Memory
    MEMORY_ROOT  = _ROOT / "MEMORY"
    MEMORY_TASKS = _ROOT / "MEMORY" / "tasks"
    MEMORY_LESSONS = _ROOT / "MEMORY" / "lessons"

    # Logs
    LOGS_DIR     = _RUNTIME / "logs"

    # State
    STATE_FILE   = _RUNTIME / "state.json"

    # Identity
    IDENTITY_FILE = _RUNTIME / "system_identity.json"

    # Projects
    PROJECTS_DIR = _ROOT / "projects"

    # Adapters
    ADAPTERS_DIR = _ROOT / "ADAPTERS"


class Models:
    """Default model identifiers per provider."""

    OPENAI_DEFAULT    = "gpt-4o-mini"
    ANTHROPIC_DEFAULT = "claude-sonnet-4-6"
    GEMINI_DEFAULT    = "gemini-2.0-flash"
    DEEPSEEK_DEFAULT  = "deepseek-chat"

    # Claude tier → model ID
    CLAUDE_TIER_MAP = {
        "haiku":  "claude-haiku-4-5-20251001",
        "sonnet": "claude-sonnet-4-6",
        "opus":   "claude-opus-4-7",
    }


APP_VERSION = "3.2.0"
