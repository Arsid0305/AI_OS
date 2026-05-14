from __future__ import annotations

import json
import logging
import os

from core.schemas import PromptConfig

logger = logging.getLogger(__name__)

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")


class AgentRegistry:
    def __init__(self):
        self.agents = {}

    def register(self, name: str, domain: str, skill: str, risk: str) -> None:
        self.agents[name] = {
            "domain": domain,
            "skill":  skill,
            "risk":   risk,
        }

    def get(self, name: str) -> dict | None:
        return self.agents.get(name)

    def list_agents(self) -> list[str]:
        return list(self.agents.keys())

    def load_prompt(self, name: str) -> PromptConfig:
        agent = self.get(name)
        if not agent:
            raise ValueError(f"Agent not registered: {name}")

        prompt_path = os.path.join(PROMPTS_DIR, agent["domain"], "v1.json")
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

        with open(prompt_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        try:
            config = PromptConfig(**raw)
        except Exception as e:
            raise ValueError(f"Invalid prompt config for '{name}': {e}") from e

        logger.debug("Prompt loaded and validated: %s", name)
        return config


def build_default_registry() -> AgentRegistry:
    reg = AgentRegistry()

    reg.register("meta_agent",  "meta_agent",  "analyzer",   "low")
    reg.register("meta_prompt", "meta_prompt", "analyzer",   "low")
    reg.register("marketplace", "marketplace", "analyzer",   "medium")
    reg.register("research",    "research",    "researcher", "low")
    reg.register("code",        "code",        "operator",   "low")
    reg.register("review",      "review",      "critic",     "low")
    reg.register("decision",    "decision",    "planner",    "medium")
    reg.register("legal",       "legal",       "analyzer",   "high")
    reg.register("medical",     "medical",     "analyzer",   "high")
    reg.register("tables",      "tables",      "operator",   "low")
    reg.register("writing",     "writing",     "writer",     "low")
    reg.register("visual",      "visual",      "planner",    "low")

    return reg
