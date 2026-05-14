from __future__ import annotations

import json
import logging
import os

from core.agent_registry import build_default_registry
from core.conflict_protocol import authorize
from core.engine.router import get_engine
from core.eval import evaluate
from core.drift import detect_drift
from core.state import save_session
from core.memory_writer import append_bug

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
_SKILLS_DIR = os.path.join(_BASE_DIR, "skills_sistem", "agents")

_CLAUDE_TIER_MAP = {
    "haiku":  "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus":   "claude-opus-4-7",
}

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
    path = os.path.join(_SKILLS_DIR, filename)
    logger.debug("SKILL LOAD: %s", path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.warning("SKILL FILE NOT FOUND: %s", filename)
        return None


def _load_skill(skill: str) -> tuple[str, str]:
    if skill not in SKILL_FILE_MAP:
        logger.warning("UNKNOWN SKILL '%s' — falling back to BOOTSTRAP", skill)
        content = _load_skill_file(BOOTSTRAP_FILE)
        return content or "", "bootstrap"

    content = _load_skill_file(SKILL_FILE_MAP[skill])
    if content:
        return content, skill

    logger.warning("SKILL FILE MISSING for '%s' — falling back to BOOTSTRAP", skill)
    content = _load_skill_file(BOOTSTRAP_FILE)
    return content or "", "bootstrap"


def _load_domain(mode: str) -> str | None:
    runtime_dir = os.path.join(_BASE_DIR, "runtime")
    path = os.path.join(runtime_dir, "prompts", mode, f"{mode}.md")
    logger.debug("DOMAIN LOAD: %s", path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
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
        agent_type: str = None,
        risk_level: str = None,
    ) -> dict:

        agent = self.registry.get(mode)
        if not agent:
            raise ValueError(f"Unknown mode: {mode}")

        skill = agent_type if agent_type else agent["skill"]
        risk  = risk_level  if risk_level  else agent["risk"]

        try:
            authorize(skill, risk)
        except Exception as e:
            logger.error("CONFLICT PROTOCOL blocked: %s", e)
            return {"content": "", "eval_score": 0.0}

        # PromptConfig — typed, validated
        prompt = self.registry.load_prompt(mode)
        system_prompt = prompt.system
        claude_tier = prompt.claude_tier
        resolved_claude_model = _CLAUDE_TIER_MAP.get(claude_tier, "claude-sonnet-4-6")

        skill_rules, active_skill = _load_skill(skill)
        if skill_rules:
            system_prompt = (
                f"MODEL TYPE: {model.upper()}\n\n"
                f"SKILL EXECUTION MODE: {active_skill.upper()}\n\n"
                f"{skill_rules}\n\n---\n\n"
                f"{system_prompt}"
            )
            logger.debug("SKILL LOADED: %s", active_skill)

        domain_rules = _load_domain(mode)
        if domain_rules:
            system_prompt = (
                f"CRITICAL DOMAIN RULES:\n\n{domain_rules}\n\n---\n\n"
                f"{system_prompt}"
            )
            logger.debug("DOMAIN LOADED for mode '%s'", mode)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt.user_template.format(input=goal)},
        ]

        engine = get_engine(model)
        if model == "anthropic":
            logger.debug("[Anthropic] tier=%s → %s", claude_tier, resolved_claude_model)
            result = engine.call(messages, temperature=temperature, model=resolved_claude_model)
        else:
            result = engine.call(messages, temperature=temperature)

        if not result or "content" not in result:
            logger.error("MODEL FAILED — returning empty safe output")
            return {"content": "", "eval_score": 0.0}

        content = result.get("content", "")

        decision_markers = ["Decision:", "Action:", "I recommend", "We should"]
        if any(m in content for m in decision_markers):
            logger.warning("ROLE DRIFT: decision marker detected in output")

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
            "mode":        mode,
            "model":       model,
            "claude_tier": claude_tier if model == "anthropic" else None,
            "skill":       active_skill,
            "risk":        risk,
            "eval_score":  eval_score,
            "drift_score": drift_details.get("score"),
            "latency":     result.get("latency"),
        }
        logger.info("ORCHESTRATOR LOG: %s", json.dumps(log, ensure_ascii=False))

        result["eval_score"] = eval_score
        return result
