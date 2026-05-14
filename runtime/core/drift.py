import re


def detect_drift(goal_text, result_text, threshold=0.2):
    """
    Drift detection: compare goal keywords with result.
    Returns (drifted: bool, details: dict).
    """
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
