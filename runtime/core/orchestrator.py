from __future__ import annotations
import json
import logging
import time
from core.config import Paths, Models
from core.agent_registry import build_default_registry
from core.conflict_protocol import authorize
from core.engine.router import get_engine
from core.eval import evaluate
from core.drift import detect_drift
from core.state import save_session
from core.memory_writer import append_bug

logger = logging.getLogger(__name__)

SKILL_FILE_MAP = {
    "analyzer":   "SKILL-01_ANALYZER.md",
    "validator":  "SKILL-02_VALIDATOR.md",
    "planner":    "SKILL-03_PLANNER.md",
    "operator":   "SKILL-04_OPERATOR.md",
    "writer":     "SKILL-05_WRITER.md",
    "researcher": "SKILL-06_RESEARCHER.md",
    "critic":     "SKILL-07_CRITIC.md",
}
BOOTSTRAP_FILE = "SKILL-00_BOOTSTRAP.md"


def _load_skill_file(filename: str) -> str | None:
    path = Paths.SKILLS_DIR / filename
    logger.debug("SKILL LOAD: %s", path)
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.warning("SKILL FILE NOT FOUND: %s", filename)
        return None


def _load_skill(skill: str) -> tuple[str, str]:
    if skill not in SKILL_FILE_MAP:
        logger.warning("UNKNOWN SKILL '%s' — falling back to BOOTSTRAP", skill)
        return _load_skill_file(BOOTSTRAP_FILE) or "", "bootstrap"
    content = _load_skill_file(SKILL_FILE_MAP[skill])
    if content:
        return content, skill
    logger.warning("SKILL FILE MISSING for '%s' — falling back to BOOTSTRAP", skill)
    return _load_skill_file(BOOTSTRAP_FILE) or "", "bootstrap"


def _load_domain(mode: str) -> str | None:
    path = Paths.PROMPTS_DIR / mode / f"{mode}.md"
    logger.debug("DOMAIN LOAD: %s", path)
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.debug("DOMAIN FILE NOT FOUND for mode '%s'", mode)
        return None


class Orchestrator:

    def __init__(self):
        self.registry = build_default_registry()

    def run(
        self,
        mode: str,
        goal: str,
        model: str = "openai",
        temperature: float = 0.2,
        agent_type: str | None = None,
        risk_level: str | None = None,
    ) -> dict:
        agent = self.registry.get(mode)
        if not agent:
            raise ValueError(f"Unknown mode: {mode}")

        skill = agent_type or agent["skill"]
        risk  = risk_level  or agent["risk"]

        try:
            authorize(skill, risk)
        except Exception as e:
            logger.error("CONFLICT PROTOCOL blocked: %s", e)
            return {"content": "", "eval_score": 0.0}

        prompt = self.registry.load_prompt(mode)
        system_prompt = prompt.system
        claude_tier   = prompt.claude_tier
        resolved_model = Models.CLAUDE_TIER_MAP.get(claude_tier, Models.ANTHROPIC_DEFAULT)

        skill_rules, active_skill = _load_skill(skill)
        if skill_rules:
            system_prompt = (
                f"MODEL TYPE: {model.upper()}\n\n"
                f"SKILL EXECUTION MODE: {active_skill.upper()}\n\n"
                f"{skill_rules}\n\n---\n\n{system_prompt}"
            )
            logger.debug("SKILL LOADED: %s", active_skill)

        domain_rules = _load_domain(mode)
        if domain_rules:
            system_prompt = f"CRITICAL DOMAIN RULES:\n\n{domain_rules}\n\n---\n\n{system_prompt}"
            logger.debug("DOMAIN LOADED for mode '%s'", mode)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt.user_template.format(input=goal)},
        ]

        engine = get_engine(model)
        result = None
        for _attempt in range(3):
            if model == "anthropic":
                logger.debug("[Anthropic] tier=%s → %s", claude_tier, resolved_model)
                result = engine.call(messages, temperature=temperature, model=resolved_model)
            else:
                result = engine.call(messages, temperature=temperature)
            if result is not None:
                break
            if _attempt < 2:
                logger.warning("Engine returned None, retry %d/3", _attempt + 2)
                time.sleep(2 ** _attempt)

        if not result or "content" not in result:
            logger.error("MODEL FAILED — returning empty safe output")
            return {"content": "", "eval_score": 0.0}

        content = result.get("content", "")

        if any(m in content for m in ["Decision:", "Action:", "I recommend", "We should"]):
            logger.warning("ROLE DRIFT: decision marker detected")

        eval_score, _ = evaluate(content, mode)

        drift_details = {"score": 1.0}
        if active_skill not in ("analyzer", "bootstrap"):
            drifted, drift_details = detect_drift(goal, content)
            if drifted:
                logger.warning("CONTENT DRIFT: score=%.2f", drift_details.get("score", 0))
                if drift_details.get("score", 1.0) < 0.3:
                    append_bug(
                        title=f"Content drift: {mode}/{active_skill}",
                        problem=f"Score {drift_details['score']:.2f} — goal: {goal[:80]}",
                        file_path="runtime/core/orchestrator.py",
                    )

        save_session(mode, model, active_skill, eval_score)

        log = {
            "mode": mode, "model": model,
            "claude_tier": claude_tier if model == "anthropic" else None,
            "skill": active_skill, "risk": risk,
            "eval_score": eval_score,
            "drift_score": drift_details.get("score"),
            "latency": result.get("latency"),
        }
        logger.info("ORCHESTRATOR LOG: %s", json.dumps(log, ensure_ascii=False))
        result["eval_score"] = eval_score
        return result
