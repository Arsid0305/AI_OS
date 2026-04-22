import os
import json
from datetime import datetime
from pathlib import Path


BASE_PATH = Path(__file__).resolve().parents[2] / "projects"


def ensure_project(project_name):
    project_path = BASE_PATH / project_name
    project_path.mkdir(parents=True, exist_ok=True)
    return project_path


def save_run(project_name, mode, content, metadata):
    project_path = ensure_project(project_name)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{mode}.txt"

    file_path = project_path / filename

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