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
        """Load versioned prompt JSON for agent's domain."""
        agent = self.get(name)
        if not agent:
            raise ValueError(f"Agent not registered: {name}")
        prompt_path = os.path.join(PROMPTS_DIR, agent["domain"], "v1.json")
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt not found: {prompt_path}")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return json.load(f)


def build_default_registry():
    """Create registry with all standard agents."""
    reg = AgentRegistry()
    reg.register("meta_agent", "meta_agent", "analyzer", "low")
    reg.register("meta_prompt", "meta_prompt", "analyzer", "low")
    reg.register("marketplace", "marketplace", "analyzer", "medium")
    reg.register("research", "research", "analyzer", "low")
    reg.register("visual", "visual", "planner", "low")
    return reg
