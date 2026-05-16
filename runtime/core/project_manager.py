"""Project manager — сохранение результатов в projects/."""
import json
from datetime import datetime
from pathlib import Path
from core.config import Paths

BASE_PATH = Paths.PROJECTS_DIR


def _safe_project_path(project_name: str) -> Path:
    """Resolve and validate path stays inside BASE_PATH (prevent traversal)."""
    resolved = (BASE_PATH / project_name).resolve()
    if not resolved.is_relative_to(BASE_PATH.resolve()):
        raise ValueError(
            f"Invalid project name '{project_name}': path must stay inside projects/"
        )
    return resolved


def ensure_project(project_name: str) -> Path:
    project_path = _safe_project_path(project_name)
    project_path.mkdir(parents=True, exist_ok=True)
    return project_path


def save_run(project_name: str, mode: str, content: str, metadata: dict) -> str:
    project_path = ensure_project(project_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = project_path / f"{timestamp}_{mode}.txt"
    full_output = (
        f"PROJECT: {project_name}\n"
        f"MODE: {mode}\n"
        f"TIMESTAMP: {timestamp}\n"
        f"METADATA:\n{json.dumps(metadata, indent=2, ensure_ascii=False)}\n\n"
        f"{'='*60}\n\n"
        f"{content}"
    )
    file_path.write_text(full_output, encoding="utf-8")
    return str(file_path)
