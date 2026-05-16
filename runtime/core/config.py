"""Central config — все пути и константы в одном месте.

Импорт: from core.config import Paths, Models
"""
from __future__ import annotations
from pathlib import Path

_ROOT    = Path(__file__).resolve().parents[2]   # repo root
_RUNTIME = Path(__file__).resolve().parents[1]   # runtime/


class Paths:
    """All filesystem paths. Absolute, computed once."""
    ROOT           = _ROOT
    RUNTIME        = _RUNTIME
    SKILLS_DIR     = _ROOT  / "skills_sistem" / "agents"
    PROMPTS_DIR    = _RUNTIME / "prompts"
    MEMORY_ROOT    = _ROOT  / "MEMORY"
    MEMORY_TASKS   = _ROOT  / "MEMORY" / "tasks"
    MEMORY_LESSONS = _ROOT  / "MEMORY" / "lessons"
    MEMORY_ARCHIVE = _ROOT  / "MEMORY" / "archive"
    LOGS_DIR       = _RUNTIME / "logs"
    STATE_FILE     = _RUNTIME / "state.json"
    IDENTITY_FILE  = _RUNTIME / "system_identity.json"
    PROJECTS_DIR   = _ROOT  / "projects"
    ADAPTERS_DIR   = _ROOT  / "ADAPTERS"


class Models:
    """Default model identifiers per provider."""
    OPENAI_DEFAULT    = "gpt-4o-mini"
    ANTHROPIC_DEFAULT = "claude-sonnet-4-6"
    GEMINI_DEFAULT    = "gemini-2.0-flash"
    DEEPSEEK_DEFAULT  = "deepseek-chat"
    CLAUDE_TIER_MAP   = {
        "haiku":  "claude-haiku-3-5-20241022",
        "sonnet": "claude-sonnet-4-6",
        "opus":   "claude-opus-4-5",
    }


APP_VERSION = "3.2.0"
