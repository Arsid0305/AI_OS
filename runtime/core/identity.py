"""Identity — проверка целостности system_identity.json."""
import json
import hashlib
from pathlib import Path
from core.config import Paths

_IDENTITY_FILE = Paths.IDENTITY_FILE


def verify_identity(path=None):
    target = Path(path) if path else _IDENTITY_FILE
    with open(target, "r", encoding="utf-8") as f:
        data = json.load(f)
    expected = data["identity_hash"]
    temp = data.copy()
    temp.pop("identity_hash")
    computed = hashlib.sha256(
        json.dumps(temp, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if computed != expected:
        raise RuntimeError("System identity integrity failure")
    return True


def generate_identity(path=None):
    """Re-compute hash after editing system_identity.json."""
    target = Path(path) if path else _IDENTITY_FILE
    with open(target, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.pop("identity_hash", None)
    h = hashlib.sha256(
        json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    data["identity_hash"] = h
    with open(target, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return h
