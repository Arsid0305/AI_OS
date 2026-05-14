"""MEMORY hygiene tool.

Mechanical rules only. No LLM. Archive-only, no deletion.
Usage: python -m core.memory_hygiene [--all | --archive-todos | --archive-bugs | --flag-stale | --report]
"""

import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path

_MEMORY_ROOT = Path(__file__).resolve().parents[2] / "MEMORY"
_ARCHIVE_ROOT = _MEMORY_ROOT / "archive"
_STALE_DAYS = 90


def _today_str() -> str:
    return date.today().strftime("%Y-%m-%d")


def _append(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)


def archive_done_todos() -> int:
    """Move done todos to archive. Returns count archived."""
    src = _MEMORY_ROOT / "tasks" / "todo.md"
    if not src.exists():
        return 0

    lines = src.read_text(encoding="utf-8").splitlines(keepends=True)
    done = [l for l in lines if l.startswith("- [x]")]
    pending = [l for l in lines if not l.startswith("- [x]")]

    if not done:
        return 0

    src.write_text("".join(pending), encoding="utf-8")

    archive_block = f"\n## Archived: {_today_str()}\n\n" + "".join(done)
    _append(_ARCHIVE_ROOT / "todo_archive.md", archive_block)

    return len(done)


def archive_closed_bugs() -> int:
    """Move closed bugs to archive. Returns count archived."""
    src = _MEMORY_ROOT / "tasks" / "bugs.md"
    if not src.exists():
        return 0

    content = src.read_text(encoding="utf-8")
    parts = re.split(r"(?=\n## \[)", content)

    open_parts = []
    closed_parts = []

    for part in parts:
        if "**Статус:** closed" in part:
            closed_parts.append(part)
        else:
            open_parts.append(part)

    if not closed_parts:
        return 0

    src.write_text("".join(open_parts), encoding="utf-8")

    archive_block = f"\n## Archived: {_today_str()}\n" + "".join(closed_parts)
    _append(_ARCHIVE_ROOT / "bugs_archive.md", archive_block)

    return len(closed_parts)


def flag_stale_decisions(stale_days: int = _STALE_DAYS) -> int:
    """Add [stale?] marker to decisions older than stale_days.

    Marker only — no semantic change, no auto-close, no auto-remove.
    """
    src = _MEMORY_ROOT / "tasks" / "decisions.md"
    if not src.exists():
        return 0

    content = src.read_text(encoding="utf-8")
    cutoff = date.today() - timedelta(days=stale_days)
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
    """Return hygiene stats as dict and print JSON to console."""

    def _count_prefix(path: Path, prefix: str) -> int:
        if not path.exists():
            return 0
        return sum(1 for l in path.read_text(encoding="utf-8").splitlines() if l.startswith(prefix))

    def _count_marker(path: Path, marker: str) -> int:
        if not path.exists():
            return 0
        return path.read_text(encoding="utf-8").count(marker)

    decisions_path = _MEMORY_ROOT / "tasks" / "decisions.md"

    stats = {
        "open_bugs":         _count_marker(_MEMORY_ROOT / "tasks" / "bugs.md", "## ["),
        "open_todos":        _count_prefix(_MEMORY_ROOT / "tasks" / "todo.md", "- [ ]"),
        "done_todos":        _count_prefix(_MEMORY_ROOT / "tasks" / "todo.md", "- [x]"),
        "lessons_count":     _count_marker(_MEMORY_ROOT / "lessons" / "lessons.md", "## ["),
        "decisions_count":   _count_marker(decisions_path, "## ["),
        "stale_decisions":   _count_marker(decisions_path, "[stale?]"),
    }

    print(json.dumps(stats, indent=2, ensure_ascii=False))
    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MEMORY hygiene tool")
    parser.add_argument("--archive-todos", action="store_true", help="Archive done todos")
    parser.add_argument("--archive-bugs",  action="store_true", help="Archive closed bugs")
    parser.add_argument("--flag-stale",    action="store_true", help="Flag stale decisions (marker only)")
    parser.add_argument("--report",        action="store_true", help="Print hygiene report")
    parser.add_argument("--all",           action="store_true", help="Run all operations + report")
    args = parser.parse_args()

    if args.all or args.archive_todos:
        n = archive_done_todos()
        print(f"✓ archived {n} done todos")
    if args.all or args.archive_bugs:
        n = archive_closed_bugs()
        print(f"✓ archived {n} closed bugs")
    if args.all or args.flag_stale:
        n = flag_stale_decisions()
        print(f"✓ flagged {n} stale decisions")
    if args.report or args.all:
        report()
