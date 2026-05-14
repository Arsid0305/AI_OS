import pytest
from core.agent_registry import build_default_registry

EXPECTED_MODES = [
    "meta_agent", "meta_prompt", "marketplace", "research",
    "visual", "code", "review", "decision", "legal", "medical", "tables", "writing",
]
VALID_SKILLS = {"analyzer", "researcher", "operator", "planner", "critic", "writer"}
VALID_RISKS  = {"low", "medium", "high"}


def test_all_modes_registered():
    reg = build_default_registry()
    for mode in EXPECTED_MODES:
        assert reg.get(mode) is not None, f"Mode '{mode}' not registered"


def test_agent_count():
    reg = build_default_registry()
    assert len(reg.list_agents()) == 12


def test_valid_skills():
    reg = build_default_registry()
    for name in reg.list_agents():
        skill = reg.get(name)["skill"]
        assert skill in VALID_SKILLS, f"Agent '{name}' has unknown skill '{skill}'"


def test_valid_risk_levels():
    reg = build_default_registry()
    for name in reg.list_agents():
        risk = reg.get(name)["risk"]
        assert risk in VALID_RISKS, f"Agent '{name}' has invalid risk '{risk}'"


def test_load_prompt_raises_for_unknown_agent():
    reg = build_default_registry()
    with pytest.raises(ValueError, match="Agent not registered"):
        reg.load_prompt("nonexistent_mode")
