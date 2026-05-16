ALLOWED_MATRIX = {
    "low": {
        "analyzer":   True,
        "validator":  True,
        "planner":    True,
        "operator":   True,
        "researcher": True,
        "writer":     True,
        "critic":     True,
    },
    "medium": {
        "analyzer":   True,
        "validator":  True,
        "planner":    True,
        "operator":   False,
        "researcher": True,
        "writer":     True,
        "critic":     True,
    },
    "high": {
        "analyzer":   True,
        "validator":  True,
        "planner":    False,
        "operator":   False,
        "researcher": True,
        "writer":     False,
        "critic":     True,
    },
}


def authorize(skill, risk):
    if risk not in ALLOWED_MATRIX:
        raise RuntimeError(f"Unknown risk level: '{risk}'. Valid: {list(ALLOWED_MATRIX.keys())}")
    allowed = ALLOWED_MATRIX[risk].get(skill, False)
    if not allowed:
        allowed_skills = [s for s, v in ALLOWED_MATRIX[risk].items() if v]
        raise RuntimeError(
            f"Conflict protocol: {skill} + {risk} risk запрещено. "
            f"Допустимые типы при {risk} risk: {', '.join(allowed_skills)}"
        )
    return True
