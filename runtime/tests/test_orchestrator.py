import pytest
from core.orchestrator import SKILL_FILE_MAP, _load_skill
from core.agent_registry import build_default_registry
from core.project_manager import _safe_project_path


def test_skill_file_map_not_empty():
    assert len(SKILL_FILE_MAP) > 0


def test_all_skill_map_keys_are_strings():
    for key, val in SKILL_FILE_MAP.items():
        assert isinstance(key, str)
        assert isinstance(val, str)
        assert val.endswith(".md"), f"Skill file should be .md: {val}"


def test_all_agent_skills_covered_by_map():
    reg = build_default_registry()
    for name in reg.list_agents():
        skill = reg.get(name)["skill"]
        assert skill in SKILL_FILE_MAP, (
            f"Agent '{name}' skill '{skill}' not in SKILL_FILE_MAP — add it or fix the agent"
        )


def test_unknown_skill_falls_back_to_bootstrap():
    _content, active = _load_skill("totally_unknown_skill_xyz")
    assert active == "bootstrap"


def test_path_traversal_blocked():
    with pytest.raises(ValueError, match="path must stay inside"):
        _safe_project_path("../../etc/passwd")


def test_path_traversal_parent_blocked():
    with pytest.raises(ValueError, match="path must stay inside"):
        _safe_project_path("../secret")


def test_valid_project_name_resolves():
    path = _safe_project_path("my_project")
    assert path.name == "my_project"
