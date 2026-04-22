import json
import os

from core.agent_registry import build_default_registry
from core.conflict_protocol import authorize
from core.engine.router import get_engine
from core.eval import evaluate
from core.drift import detect_drift

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
_SKILLS_DIR = os.path.join(_BASE_DIR, "skills_sistem", "agents")

SKILL_FILE_MAP = {
    "analyzer":  "SKILL-01_ANALYZER.md",
    "validator": "SKILL-02_VALIDATOR.md",
    "planner":   "SKILL-03_PLANNER.md",
    "operator":  "SKILL-04_OPERATOR.md",
}

BOOTSTRAP_FILE = "SKILL-00_BOOTSTRAP.md"


def _load_skill_file(filename: str) -> str | None:
    path = os.path.join(_SKILLS_DIR, filename)
    print(f">>> SKILL LOAD: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f">>> SKILL FILE NOT FOUND: {filename}")
        return None


def _load_skill(skill: str) -> tuple[str, str]:
    """
    Загрузить skill по имени.
    Если skill не найден в карте — использовать BOOTSTRAP как fallback.
    Возвращает (содержимое файла, фактическое имя skill).
    """
    skill_file = SKILL_FILE_MAP.get(skill)

    if skill_file:
        content = _load_skill_file(skill_file)
        if content:
            return content, skill

    # BOOTSTRAP FALLBACK
    print(f">>> SKILL '{skill}' not found → BOOTSTRAP fallback")
    content = _load_skill_file(BOOTSTRAP_FILE)
    return content or "", "bootstrap"


def _load_domain(mode: str) -> str | None:
    runtime_dir = os.path.join(_BASE_DIR, "runtime")
    path = os.path.join(runtime_dir, "prompts", mode, f"{mode}.md")
    print(f">>> DOMAIN LOAD: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(">>> DOMAIN FILE NOT FOUND")
        return None


class Orchestrator:

    def __init__(self):
        self.registry = build_default_registry()

    def run(self, mode: str, goal: str, model: str = "openai", temperature: float = 0.2) -> dict:

        agent = self.registry.get(mode)
        if not agent:
            raise ValueError(f"Unknown mode: {mode}")

        skill = agent["skill"]
        risk  = agent["risk"]

        authorize(skill, risk)

        prompt_data = self.registry.load_prompt(mode)
        system_prompt = prompt_data["system"]

        # === SKILL INJECTION (с BOOTSTRAP fallback) ===
        skill_rules, active_skill = _load_skill(skill)
        if skill_rules:
            system_prompt = (
                f"MODEL TYPE: {model.upper()}\n\n"
                f"SKILL EXECUTION MODE: {active_skill.upper()}\n\n"
                f"{skill_rules}\n\n---\n\n"
                f"{system_prompt}"
            )
            print(f">>> SKILL LOADED: {active_skill}")

        # === DOMAIN INJECTION ===
        domain_rules = _load_domain(mode)
        if domain_rules:
            system_prompt = (
                f"CRITICAL DOMAIN RULES:\n\n{domain_rules}\n\n---\n\n"
                f"{system_prompt}"
            )
            print(">>> DOMAIN LOADED")

        # === BUILD MESSAGES ===
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt_data["user_template"].format(input=goal)},
        ]

        # === ENGINE CALL ===
        engine = get_engine(model)
        result = engine.call(messages, temperature=temperature)

        if not result or "content" not in result:
            print("⛔ MODEL FAILED → returning empty safe output")
            return {"content": "", "eval_score": 0.0}

        content = result.get("content", "")

        # === ROLE DRIFT DETECTION ===
        decision_markers = ["Decision:", "Action:", "I recommend", "We should"]
        if any(m in content for m in decision_markers):
            print("⚠️ ROLE DRIFT: decision detected")

        # === EVALUATION ===
        eval_score, _ = evaluate(content, mode)

        if active_skill in ("analyzer", "bootstrap"):
            drift_details = {"score": 0.0}
        else:
            _, drift_details = detect_drift(goal, content)

        log = {
            "mode":        mode,
            "model":       model,
            "skill":       active_skill,
            "risk":        risk,
            "eval_score":  eval_score,
            "drift_score": drift_details.get("score"),
            "latency":     result.get("latency"),
        }
        print("\n🧠 ORCHESTRATOR LOG")
        print(json.dumps(log, indent=2, ensure_ascii=False))

        result["eval_score"] = eval_score
        return result
