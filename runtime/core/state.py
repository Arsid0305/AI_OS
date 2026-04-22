"""State — персистентное хранилище key-value между запусками.

Файл: runtime/state.json

Использование:
    from core.state import save_state, load_state

    save_state("last_mode", "research")
    mode = load_state("last_mode", default="meta_agent")
"""

import json
from pathlib import Path

_STATE_FILE = Path(__file__).resolve().parents[1] / "state.json"


def save_state(key: str, value):
    data = _read()
    data[key] = value
    _write(data)


def load_state(key: str, default=None):
    return _read().get(key, default)


def clear_state(key: str = None):
    """Удалить один ключ или очистить всё (key=None)."""
    if key is None:
        _write({})
    else:
        data = _read()
        data.pop(key, None)
        _write(data)


def _read() -> dict:
    if not _STATE_FILE.exists():
        return {}
    try:
        return json.loads(_STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write(data: dict):
    _STATE_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
