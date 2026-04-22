import re


def detect_drift(goal_text, result_text, threshold=0.2):
    """
    Drift detection logic:

    1. If strict authoritative numeric block is present → no drift.
    2. Otherwise compare goal keywords with result text.
    """

    # Strict mode override
    if "STRICT NUMERIC CALCULATION" in result_text or "Python authoritative" in result_text:
        return False, {
            "score": 1.0,
            "reason": "strict_block_present",
            "matched": [],
            "missed": []
        }

    tokens = re.findall(r"\w+", goal_text.lower())
    matched = []
    missed = []

    for t in set(tokens):
        if len(t) < 3:
            continue
        if t in result_text.lower():
            matched.append(t)
        else:
            missed.append(t)

    total = len(matched) + len(missed)
    score = len(matched) / total if total > 0 else 1.0

    drifted = score < (1 - threshold)

    return drifted, {
        "score": round(score, 2),
        "matched": matched,
        "missed": missed
    }