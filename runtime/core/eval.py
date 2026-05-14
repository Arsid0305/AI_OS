import re

EVAL_RULES = {
    "meta_agent": {
        "min_length": 500,
        "sections": [
            (["role", "роль"], "Role"),
            (["task", "задача", "objective"], "Task"),
            (["process", "процесс", "step", "шаг"], "Process"),
            (["constraint", "ограничен", "forbidden", "запрещ"], "Constraints"),
            (["input", "вход"], "Input"),
            (["output", "выход"], "Output"),
        ],
    },
    "meta_prompt": {
        "min_length": 300,
        "sections": [
            (["role", "роль"], "Role"),
            (["objective", "цель", "task"], "Objective"),
            (["constraint", "ограничен"], "Constraints"),
            (["process", "процесс"], "Process"),
            (["output", "format", "формат"], "Output format"),
        ],
    },
    "marketplace": {
        "min_length": 200,
        "sections": [
            (["metric", "метрик", "kpi", "revenue", "ctr", "margin"], "KPI"),
            (["recommend", "рекоменд", "action", "действ"], "Recommendations"),
        ],
    },
    "research": {
        "min_length": 300,
        "sections": [
            (["context", "контекст", "chronolog", "хронолог"], "Context"),
            (["structur", "структур", "cluster", "кластер", "map"], "Structure"),
            (["risk", "риск", "implication", "вывод"], "Risk/Implications"),
        ],
    },
    "visual": {
        "min_length": 200,
        "sections": [
            (["prompt", "промпт"], "Prompts"),
            (["variant", "вариант", "a/b"], "Variants"),
        ],
    },
    "code": {
        "min_length": 50,
        "sections": [
            (["```", "def ", "class ", "function", "const ", "var "], "Code block"),
            (["decision", "решение", "because", "потому что", "reason"], "Key decision"),
        ],
    },
    "decision": {
        "min_length": 200,
        "sections": [
            (["option", "вариант", "alternative", "альтернатив"], "Options"),
            (["recommend", "рекоменд", "suggest", "предлаг"], "Recommendation"),
            (["risk", "риск", "tradeoff", "компромисс"], "Risks"),
        ],
    },
    "legal": {
        "min_length": 300,
        "sections": [
            (["риск", "risk", "нарушен"], "Risks"),
            (["рекоменд", "recommend", "формулировк"], "Recommendations"),
            (["закон", "фз", "статья", "law", "article"], "Legal reference"),
        ],
    },
    "medical": {
        "min_length": 200,
        "sections": [
            (["норма", "отклонение", "normal", "reference"], "Norm/deviation"),
            (["врач", "специалист", "doctor", "specialist"], "Doctor referral"),
        ],
    },
    "review": {
        "min_length": 150,
        "sections": [
            (["проблема", "issue", "problem", "ошибка"], "Issues"),
            (["рекоменд", "fix", "исправ", "suggest"], "Fixes"),
        ],
    },
    "tables": {
        "min_length": 50,
        "sections": [
            (["формула", "formula", "=if", "=sum", "=vlookup"], "Formula"),
            (["ячейка", "cell", "column", "столбец"], "Cell reference"),
        ],
    },
    "writing": {
        "min_length": 100,
        "sections": [
            ([".", "\n"], "Has content"),
        ],
    },
}


def evaluate(content, mode="research"):
    """Evaluate output quality. Returns (score, checks_dict)."""
    rules = EVAL_RULES.get(mode, EVAL_RULES["research"])
    checks = {}
    text_lower = content.lower()

    checks["min_length"] = len(content) >= rules["min_length"]
    checks["has_structure"] = len(re.findall(r"^#{1,3}\s+", content, re.MULTILINE)) >= 2
    checks["non_empty"] = len(content.strip()) > 0

    for keywords, label in rules["sections"]:
        checks[f"has_{label}"] = any(kw in text_lower for kw in keywords)

    score = sum(checks.values()) / len(checks) if checks else 0
    return round(score, 2), checks
