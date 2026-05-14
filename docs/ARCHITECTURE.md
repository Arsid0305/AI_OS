# AI_OS — Архитектура (финал)

> Актуально на: 2026-05-14

```
AI_OS/
│
├── ── CORE ───────────────────────────────────────
│   └── SYSTEM.md                  ← универсальные правила (любой AI)
│
├── ── ADAPTERS ──────────────────────────────────────
│   ├── CLAUDE.md                  ← Claude Code adapter (в корне репо)
│   └── ADAPTERS/
│       ├── chatgpt/BOOTSTRAP.md   ← ChatGPT
│       ├── claude-web/BOOTSTRAP.md← Claude.ai
│       ├── gemini/GEMINI.md       ← Gemini
│       └── codex/BOOTSTRAP.md     ← Codex
│
├── ── MEMORY ────────────────────────────────────────
│   ├── tasks/
│   │   ├── bugs.md                ← открытые баги (dedup по title)
│   │   ├── todo.md                ← активные задачи
│   │   └── decisions.md           ← архитектурные решения
│   ├── lessons/
│   │   └── lessons.md             ← накопленные уроки
│   └── archive/                   ← hygiene output
│
├── ── RUNTIME ───────────────────────────────────────
│   ├── main.py                    ← CLI entry (--diagnose / --mode)
│   ├── system_identity.json       ← integrity hash
│   ├── requirements.txt
│   ├── logs/                      ← structured logs
│   ├── core/
│   │   ├── config.py              ← Paths + Models (единый источник)
│   │   ├── schemas.py             ← Pydantic PromptConfig
│   │   ├── startup.py             ← валидация при старте
│   │   ├── diagnostics.py         ← --diagnose вывод
│   │   ├── logger.py              ← console + file logging
│   │   ├── identity.py            ← integrity check
│   │   ├── orchestrator.py        ← routing + skill injection
│   │   ├── agent_registry.py      ← 12 режимов
│   │   ├── conflict_protocol.py   ← risk authorization
│   │   ├── drift.py               ← content drift detection
│   │   ├── eval.py                ← output evaluation
│   │   ├── state.py               ← session state (JSON)
│   │   ├── memory_writer.py       ← runtime → MEMORY bridge
│   │   ├── memory_hygiene.py      ← lifecycle / archive
│   │   ├── project_manager.py     ← save runs (path traversal guard)
│   │   ├── unit_calc.py           ← marketplace calculations
│   │   └── engine/
│   │       ├── base_engine.py     ← абстрактный контракт (**kwargs)
│   │       ├── router.py          ← провайдер по имени модели
│   │       ├── openai_engine.py
│   │       ├── anthropic_engine.py
│   │       ├── gemini_engine.py
│   │       └── deepseek_engine.py
│   ├── prompts/                   ← 12 папок × v1.json (PromptConfig)
│   └── tests/
│       ├── conftest.py
│       ├── test_registry.py
│       ├── test_prompts.py
│       ├── test_orchestrator.py
│       └── test_startup.py
│
├── ── SKILLS ────────────────────────────────────────
│   └── skills_sistem/agents/
│       ├── SKILL-00_BOOTSTRAP.md
│       ├── SKILL-01_ANALYZER.md
│       ├── SKILL-02_VALIDATOR.md
│       ├── SKILL-03_PLANNER.md
│       ├── SKILL-04_OPERATOR.md
│       ├── SKILL-05_WRITER.md
│       ├── SKILL-06_RESEARCHER.md
│       └── SKILL-07_CRITIC.md
│
├── ── APPLICATIONS ──────────────────────────────────
│   └── projects/
│       └── WB_BOT/                ← бот для ответов на Wildberries / Ozon
│
├── ── DOCS ──────────────────────────────────────────
│   └── docs/
│       ├── ARCHITECTURE.md        ← архитектура системы (этот файл)
│       ├── AI_TESTING.md          ← инструкция по тестированию AI
│       ├── ai_benchmark.md        ← результаты тестов (прогоны)
│       ├── памятка.md             ← памятка по работе с AI_OS
│       └── SESSION_EPICRISIS.md   ← контекст сессии аудита
│
└── ── CI/CD ─────────────────────────────────────────
    └── .github/workflows/
        ├── automerge.yml          ← claude/... → dev
        └── promote.yml            ← dev → main

```

---

## Движки (engine/)

| Провайдер | Алиас `--model` | Ключ |
|---|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` |
| Anthropic | `anthropic`, `claude` | `ANTHROPIC_API_KEY` |
| Gemini | `gemini` | `GOOGLE_API_KEY` |
| DeepSeek | `deepseek` | `DEEPSEEK_API_KEY` |

Формат вывода (обязателен для всех движков):
```python
{
    "content": str,
    "model": str,
    "latency": float,
    "tokens_prompt": int,
    "tokens_completion": int
}
```

---

## Режимы (12)

`meta_agent` `meta_prompt` `marketplace` `research` `visual`
`code` `review` `decision` `legal` `medical` `tables` `writing`

---

## Запуск

```bash
cd runtime
python main.py --diagnose                              # проверка системы
python main.py --mode code --model openai --goal "..."
python main.py --mode code --model claude --goal "..."
pytest tests/                                          # smoke tests
```

---

## Как расширять

**Новый режим:**
1. `prompts/режим/v1.json` (поля: system, user_template, claude_tier)
2. Строка в `agent_registry.py`
3. Добавить в `MODES` в `main.py`

**Новый движок:**
1. `engine/новый_engine.py` → унаследовать `BaseEngine`
2. Строка в `router.py` и `startup.py`

**Новый скил:**
1. `skills_sistem/agents/SKILL-0N_*.md`
2. Строка в `SKILL_FILE_MAP` в `orchestrator.py`

> Все пути — только через `Paths` из `core/config.py`. После изменений — `pytest tests/`.
