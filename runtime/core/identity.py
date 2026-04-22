"""Identity — проверка целостности system_identity.json.

Путь к файлу вычисляется абсолютно от расположения этого модуля,
поэтому скрипт можно запускать из любой директории.
"""

import json
import hashlib
from pathlib import Path

# runtime/system_identity.json — всегда относительно этого файла
_IDENTITY_FILE = Path(__file__).resolve().parents[1] / "system_identity.json"


def verify_identity(path=None):
    target = Path(path) if path else _IDENTITY_FILE
    with open(target, "r", encoding="utf-8") as f:
        data = json.load(f)
    expected = data["identity_hash"]
    temp = data.copy()
    temp.pop("identity_hash")
    computed = hashlib.sha256(json.dumps(temp, sort_keys=True).encode()).hexdigest()
    if computed != expected:
        raise RuntimeError("System identity integrity failure")
    return True


def generate_identity(path=None):
    """Пересчитать хэш после редактирования system_identity.json."""
    target = Path(path) if path else _IDENTITY_FILE
    with open(target, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.pop("identity_hash", None)
    h = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    data["identity_hash"] = h
    with open(target, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return h
