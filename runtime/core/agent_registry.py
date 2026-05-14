import json
import os

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")


class AgentRegistry:
    def __init__(self):
        self.agents = {}

    def register(self, name, domain, skill, risk):
        self.agents[name] = {
            "domain": domain,
            "skill": skill,
            "risk": risk,
        }

    def get(self, name):
        return self.agents.get(name)

    def list_agents(self):
        return list(self.agents.keys())

    def load_prompt(self, name):
        agent = self.get(name)
        if not agent:
            raise ValueError(f"Agent not registered: {name}")
        prompt_path = os.path.join(PROMPTS_DIR, agent["domain"], "v1.json")
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt not found: {prompt_path}")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return json.load(f)


def build_default_registry():
    reg = AgentRegistry()

    # анализ и исследования
    reg.register("meta_agent",  "meta_agent",  "analyzer", "low")
    reg.register("meta_prompt", "meta_prompt", "analyzer", "low")
    reg.register("marketplace", "marketplace", "analyzer", "medium")
    reg.register("research",    "research",    "researcher", "low")
    reg.register("code",        "code",        "operator",  "low")
    reg.register("review",      "review",      "critic",    "low")
    reg.register("decision",    "decision",    "planner",   "medium")

    # специализированные домены
    reg.register("legal",       "legal",       "analyzer",  "high")
    reg.register("medical",     "medical",     "analyzer",  "high")
    reg.register("tables",      "tables",      "operator",  "low")
    reg.register("writing",     "writing",     "writer",    "low")
    reg.register("visual",      "visual",      "planner",   "low")

    return reg
