"""Persistent writes to MEMORY/ markdown files.

Append-only. Never overwrites existing content.
Use state.py for ephemeral runtime state.
"""

import re
from datetime import date
from pathlib import Path

_MEMORY_ROOT = Path(__file__).resolve().parents[2] / "MEMORY"


def _today() -> str:
    return date.today().strftime("%Y-%m-%d")


def _append(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)


def _file_contains(path: Path, text: str) -> bool:
    if not path.exists():
        return False
    return text in path.read_text(encoding="utf-8")


def append_bug(title: str, problem: str, file_path: str = "") -> None:
    """Append to MEMORY/tasks/bugs.md. Deduplicates by title — no spam."""
    path = _MEMORY_ROOT / "tasks" / "bugs.md"
    if _file_contains(path, f"## [{_today()}] {title}"):
        return
    entry = (
        f"\n## [{_today()}] {title}\n"
        f"**Проблема:** {problem}\n"
        f"**Файл:** {file_path}\n"
        f"**Статус:** open\n"
    )
    _append(path, entry)


def close_bug(title: str) -> bool:
    """Mark a bug as closed by title. Returns True if found and updated."""
    path = _MEMORY_ROOT / "tasks" / "bugs.md"
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8")
    if title not in content:
        return False
    pattern = r"## \[\d{4}-\d{2}-\d{2}\] " + re.escape(title)
    match = re.search(pattern, content)
    if not match:
        return False
    start = match.start()
    section = content[start:]
    updated_section = section.replace("**Статус:** open", "**Статус:** closed", 1)
    if updated_section == section:
        return False
    path.write_text(content[:start] + updated_section, encoding="utf-8")
    return True


def append_lesson(title: str, what_happened: str, rule: str) -> None:
    """Append to MEMORY/lessons/lessons.md."""
    path = _MEMORY_ROOT / "lessons" / "lessons.md"
    entry = (
        f"\n## [{_today()}] {title}\n"
        f"**Что произошло:** {what_happened}\n"
        f"**Правило:** {rule}\n"
    )
    _append(path, entry)


def append_decision(
    title: str, context: str, decision: str, reason: str, alternatives: str = ""
) -> None:
    """Append to MEMORY/tasks/decisions.md."""
    path = _MEMORY_ROOT / "tasks" / "decisions.md"
    entry = (
        f"\n## [{_today()}] {title}\n"
        f"**Контекст:** {context}\n"
        f"**Решение:** {decision}\n"
        f"**Причина:** {reason}\n"
    )
    if alternatives:
        entry += f"**Альтернативы:** {alternatives}\n"
    _append(path, entry)


def update_todo_done(task_text: str) -> None:
    """Mark todo as done. State transition only — preserves timeline."""
    path = _MEMORY_ROOT / "tasks" / "todo.md"
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    updated = content.replace(f"- [ ] {task_text}", f"- [x] {task_text}", 1)
    if updated != content:
        path.write_text(updated, encoding="utf-8")
