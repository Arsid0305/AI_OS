"""MEMORY hygiene tool.

Mechanical rules only. No LLM. Archive-only, no deletion.
Usage: python -m core.memory_hygiene [--all | --archive-todos | --archive-bugs | --flag-stale | --report]
"""
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from core.config import Paths

_MEMORY_ROOT  = Paths.MEMORY_ROOT
_ARCHIVE_ROOT = Paths.MEMORY_ARCHIVE
_STALE_DAYS   = 90


def _today_str() -> str:
    return date.today().strftime("%Y-%m-%d")


def _append(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)


def archive_done_todos() -> int:
    src = _MEMORY_ROOT / "tasks" / "todo.md"
    if not src.exists():
        return 0
    lines = src.read_text(encoding="utf-8").splitlines(keepends=True)
    done    = [l for l in lines if l.startswith("- [x]")]
    pending = [l for l in lines if not l.startswith("- [x]")]
    if not done:
        return 0
    src.write_text("".join(pending), encoding="utf-8")
    _append(_ARCHIVE_ROOT / "todo_archive.md",
            f"\n## Archived: {_today_str()}\n\n" + "".join(done))
    return len(done)


def archive_closed_bugs() -> int:
    src = _MEMORY_ROOT / "tasks" / "bugs.md"
    if not src.exists():
        return 0
    content = src.read_text(encoding="utf-8")
    parts = re.split(r"(?=\n## \[)", content)
    open_parts   = [p for p in parts if "**Статус:** closed" not in p]
    closed_parts = [p for p in parts if "**Статус:** closed" in p]
    if not closed_parts:
        return 0
    _append(_ARCHIVE_ROOT / "bugs_archive.md",
            f"\n## Archived: {_today_str()}\n" + "".join(closed_parts))
    src.write_text("".join(open_parts), encoding="utf-8")
    return len(closed_parts)


def flag_stale_decisions(stale_days: int = _STALE_DAYS) -> int:
    src = _MEMORY_ROOT / "tasks" / "decisions.md"
    if not src.exists():
        return 0
    content = src.read_text(encoding="utf-8")
    cutoff  = date.today() - timedelta(days=stale_days)
    flagged = 0

    def _flag(m: re.Match) -> str:
        nonlocal flagged
        date_str, title = m.group(1), m.group(2)
        if "[stale?]" in title:
            return m.group(0)
        try:
            entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return m.group(0)
        if entry_date < cutoff:
            flagged += 1
            return f"## [{date_str}] {title.rstrip()} [stale?]"
        return m.group(0)

    updated = re.sub(r"## \[(\d{4}-\d{2}-\d{2})\] (.+)", _flag, content)
    if flagged:
        src.write_text(updated, encoding="utf-8")
    return flagged


def report() -> dict:
    def _count_prefix(path: Path, prefix: str) -> int:
        if not path.exists():
            return 0
        return sum(1 for l in path.read_text(encoding="utf-8").splitlines() if l.startswith(prefix))

    def _count_open_bug_sections(path: Path) -> int:
        if not path.exists():
            return 0
        content = path.read_text(encoding="utf-8")
        sections = re.split(r"(?=\n## \[)", content)
        return sum(
            1 for s in sections
            if re.search(r"^## \[", s, re.MULTILINE)
            and "CLOSED" not in s
            and "[x]" not in s
            and "**Статус:** closed" not in s
        )

    def _count_marker(path: Path, marker: str) -> int:
        if not path.exists():
            return 0
        return path.read_text(encoding="utf-8").count(marker)

    decisions_path = _MEMORY_ROOT / "tasks" / "decisions.md"
    stats = {
        "open_bugs":       _count_open_bug_sections(_MEMORY_ROOT / "tasks" / "bugs.md"),
        "open_todos":      _count_prefix(_MEMORY_ROOT / "tasks" / "todo.md", "- [ ]"),
        "done_todos":      _count_prefix(_MEMORY_ROOT / "tasks" / "todo.md", "- [x]"),
        "lessons_count":   _count_marker(_MEMORY_ROOT / "lessons" / "lessons.md", "## ["),
        "decisions_count": _count_marker(decisions_path, "## ["),
        "stale_decisions": _count_marker(decisions_path, "[stale?]"),
    }
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    return stats


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MEMORY hygiene tool")
    parser.add_argument("--archive-todos", action="store_true")
    parser.add_argument("--archive-bugs",  action="store_true")
    parser.add_argument("--flag-stale",    action="store_true")
    parser.add_argument("--report",        action="store_true")
    parser.add_argument("--all",           action="store_true")
    args = parser.parse_args()
    if args.all or args.archive_todos:
        print(f"✓ archived {archive_done_todos()} done todos")
    if args.all or args.archive_bugs:
        print(f"✓ archived {archive_closed_bugs()} closed bugs")
    if args.all or args.flag_stale:
        print(f"✓ flagged {flag_stale_decisions()} stale decisions")
    if args.report or args.all:
        report()
