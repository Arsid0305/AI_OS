"""Runtime diagnostics — быстрая проверка состояния системы."""
from __future__ import annotations
import json
import os
from pathlib import Path
from core.config import Paths, Models, APP_VERSION

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

_API_KEYS = [
    ("openai",    "OPENAI_API_KEY"),
    ("anthropic", "ANTHROPIC_API_KEY"),
    ("gemini",    "GOOGLE_API_KEY"),
    ("deepseek",  "DEEPSEEK_API_KEY"),
]

_REQUIRED_DIRS = [
    ("skills_sistem/agents", Paths.SKILLS_DIR),
    ("runtime/prompts",      Paths.PROMPTS_DIR),
    ("MEMORY/tasks",         Paths.MEMORY_TASKS),
    ("MEMORY/lessons",       Paths.MEMORY_LESSONS),
    ("runtime/logs",         Paths.LOGS_DIR),
]


def _ok(label: str) -> str:
    return f"  ✓ {label}"


def _fail(label: str) -> str:
    return f"  ✗ {label}"


def run_diagnostics() -> None:
    lines: list[str] = []

    lines.append(f"AI_OS v{APP_VERSION}")
    lines.append("-" * 40)

    # Identity
    lines.append("\nIdentity:")
    if Paths.IDENTITY_FILE.exists():
        try:
            data = json.loads(Paths.IDENTITY_FILE.read_text(encoding="utf-8"))
            h = data.get("identity_hash", "?")[:16]
            lines.append(_ok(f"system_identity.json  hash={h}..."))
        except Exception as e:
            lines.append(_fail(f"system_identity.json  parse error: {e}"))
    else:
        lines.append(_fail("system_identity.json  NOT FOUND"))

    # API keys
    lines.append("\nAPI keys:")
    for provider, key_name in _API_KEYS:
        val = os.getenv(key_name, "").strip()
        if val:
            lines.append(_ok(f"{provider:<10} {key_name} = {val[:8]}..."))
        else:
            lines.append(_fail(f"{provider:<10} {key_name} NOT SET"))

    # Directories
    lines.append("\nDirectories:")
    for label, path in _REQUIRED_DIRS:
        if path.exists():
            lines.append(_ok(label))
        else:
            lines.append(_fail(f"{label}  MISSING"))

    # Prompts
    lines.append("\nPrompts:")
    if Paths.PROMPTS_DIR.exists():
        prompt_dirs = sorted(p for p in Paths.PROMPTS_DIR.iterdir() if p.is_dir())
        for d in prompt_dirs:
            v1 = d / "v1.json"
            if not v1.exists():
                lines.append(_fail(f"{d.name}/v1.json  MISSING"))
                continue
            try:
                raw = json.loads(v1.read_text(encoding="utf-8"))
                ok = raw.get("system", "").strip() and "{input}" in raw.get("user_template", "")
                if ok:
                    lines.append(_ok(f"{d.name}/v1.json"))
                else:
                    lines.append(_fail(f"{d.name}/v1.json  invalid schema"))
            except json.JSONDecodeError:
                lines.append(_fail(f"{d.name}/v1.json  INVALID JSON"))
    else:
        lines.append(_fail("prompts/ directory missing"))

    # Skills
    lines.append("\nSkills:")
    for filename in _SKILL_FILES:
        path = Paths.SKILLS_DIR / filename
        if path.exists():
            lines.append(_ok(filename))
        else:
            lines.append(_fail(f"{filename}  MISSING"))

    lines.append("\n" + "-" * 40)
    issues = sum(1 for l in lines if l.startswith("  ✗"))
    if issues == 0:
        lines.append("✅ All checks passed")
    else:
        lines.append(f"⚠️  {issues} issue(s) found")

    print("\n".join(lines))
