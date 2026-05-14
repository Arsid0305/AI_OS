import json
import pytest
from core.config import Paths
from core.schemas import PromptConfig


def _prompt_dirs():
    if not Paths.PROMPTS_DIR.exists():
        return []
    return sorted(p for p in Paths.PROMPTS_DIR.iterdir() if p.is_dir())


@pytest.mark.parametrize("prompt_dir", _prompt_dirs(), ids=lambda p: p.name)
def test_prompt_v1_exists(prompt_dir):
    assert (prompt_dir / "v1.json").exists(), f"v1.json missing in {prompt_dir.name}/"


@pytest.mark.parametrize("prompt_dir", _prompt_dirs(), ids=lambda p: p.name)
def test_prompt_json_parseable(prompt_dir):
    v1 = prompt_dir / "v1.json"
    if not v1.exists():
        pytest.skip("v1.json missing")
    raw = json.loads(v1.read_text(encoding="utf-8"))
    assert isinstance(raw, dict), "Prompt must be a JSON object"


@pytest.mark.parametrize("prompt_dir", _prompt_dirs(), ids=lambda p: p.name)
def test_prompt_passes_schema(prompt_dir):
    v1 = prompt_dir / "v1.json"
    if not v1.exists():
        pytest.skip("v1.json missing")
    raw = json.loads(v1.read_text(encoding="utf-8"))
    config = PromptConfig(**raw)  # raises ValidationError if invalid
    assert config.system.strip(), "system prompt is empty"
    assert "{input}" in config.user_template, "user_template missing {input}"
