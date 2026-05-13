"""State — персистентное хранилище key-value между запусками.

Только для следующего: last_mode, last_model, eval_score.
Не использовать для истории чатов, полных логов или knowledge. Для этого — memory_writer.py.

Файл: runtime/state.json
Использование:
    from core.state import save_state, load_state, save_session, load_last_session
"""

import json
from pathlib import Path

_STATE_FILE = Path(__file__).resolve().parents[1] / "state.json"
_SESSION_KEY = "last_session"


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


def save_session(mode: str, model: str, skill: str, eval_score: float) -> None:
    """Save minimal operational session metadata for continuity."""
    save_state(_SESSION_KEY, {
        "last_mode": mode,
        "last_model": model,
        "last_skill": skill,
        "last_eval_score": eval_score,
    })


def load_last_session() -> dict:
    """Load last session metadata. Returns empty dict if none."""
    return load_state(_SESSION_KEY, default={})


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
