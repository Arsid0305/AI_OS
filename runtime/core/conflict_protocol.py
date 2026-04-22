ALLOWED_MATRIX = {
    "low": {"analyzer": True, "validator": True, "planner": True, "operator": True},
    "medium": {"analyzer": True, "validator": True, "planner": True, "operator": False},
    "high": {"analyzer": True, "validator": True, "planner": False, "operator": False},
}


def authorize(skill, risk):
    allowed = ALLOWED_MATRIX.get(risk, {}).get(skill, False)
    if not allowed:
        allowed_skills = [s for s, v in ALLOWED_MATRIX.get(risk, {}).items() if v]
        raise RuntimeError(
            f"Conflict protocol: {skill} + {risk} risk запрещено. "
            f"Допустимые типы при {risk} risk: {', '.join(allowed_skills)}"
        )
    return True
