"""State — персистентное key-value хранилище между запусками."""
import json
import logging
from core.config import Paths

_STATE_FILE = Paths.STATE_FILE
_SESSION_KEY = "last_session"

logger = logging.getLogger(__name__)


def save_state(key: str, value) -> None:
    data = _read()
    data[key] = value
    _write(data)


def load_state(key: str, default=None):
    return _read().get(key, default)


def clear_state(key: str = None) -> None:
    if key is None:
        _write({})
    else:
        data = _read()
        data.pop(key, None)
        _write(data)


def save_session(mode: str, model: str, skill: str, eval_score: float) -> None:
    save_state(_SESSION_KEY, {
        "last_mode":       mode,
        "last_model":      model,
        "last_skill":      skill,
        "last_eval_score": eval_score,
    })


def load_last_session() -> dict:
    return load_state(_SESSION_KEY, default={})


def _read() -> dict:
    if not _STATE_FILE.exists():
        return {}
    try:
        return json.loads(_STATE_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("state.json unreadable: %s", e)
        return {}


def _write(data: dict) -> None:
    tmp = _STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(_STATE_FILE)
