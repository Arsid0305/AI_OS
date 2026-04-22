"""Logger — запись событий в консоль и файл.

Лог-файл: runtime/logs/ai_os.log
Ротация: новый файл каждый день (суффикс даты).
"""

import json
from datetime import datetime, date
from pathlib import Path

_LOGS_DIR = Path(__file__).resolve().parents[1] / "logs"


def _get_log_file() -> Path:
    _LOGS_DIR.mkdir(exist_ok=True)
    return _LOGS_DIR / f"ai_os_{date.today().isoformat()}.log"


def log_event(data: dict):
    data = dict(data)  # не мутируем оригинал
    data["timestamp"] = datetime.utcnow().isoformat()

    line = json.dumps(data, ensure_ascii=False)

    # Консоль
    print(line)

    # Файл
    try:
        with open(_get_log_file(), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"⚠️ Logger write error: {e}")
