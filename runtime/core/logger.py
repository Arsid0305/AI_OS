"""Logger — центральная настройка logging для AI_OS."""
import json
import logging
from datetime import datetime, date, timezone
from core.config import Paths


def _setup_logging() -> None:
    Paths.LOGS_DIR.mkdir(exist_ok=True)
    log_file = Paths.LOGS_DIR / f"ai_os_{date.today().isoformat()}.log"
    fmt = "%(asctime)s %(levelname)-8s %(name)s — %(message)s"
    datefmt = "%H:%M:%S"
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(fmt, datefmt))
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(fmt, datefmt))
    root = logging.getLogger()
    if not root.handlers:
        root.setLevel(logging.DEBUG)
        root.addHandler(console)
        root.addHandler(file_handler)


_setup_logging()
_logger = logging.getLogger("ai_os")


def log_event(data: dict) -> None:
    data = dict(data)
    data["timestamp"] = datetime.now(timezone.utc).isoformat()
    _logger.info(json.dumps(data, ensure_ascii=False))
