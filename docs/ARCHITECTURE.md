# AI_OS — Архитектура движка (мультимодельная)

## Структура core/engine/

```
core/engine/
  __init__.py
  base_engine.py        ← Контракт: абстрактный BaseEngine.call()
  openai_engine.py      ← Реализация: OpenAI SDK
  anthropic_engine.py   ← Реализация: Anthropic SDK (Claude)
  router.py             ← Маршрутизатор по имени модели
```

## Как добавить новый движок

1. Создать `core/engine/gemini_engine.py`
2. Унаследовать `BaseEngine`
3. Реализовать `call(messages, temperature) -> dict | None`
4. Добавить в `router.py`:
   ```python
   elif model == "gemini":
       from core.engine.gemini_engine import GeminiEngine
       return GeminiEngine()
   ```

## Формат вывода (обязателен для всех движков)

```python
{
    "content": str,          # текст ответа
    "model": str,            # идентификатор модели
    "latency": float,        # секунды
    "tokens_prompt": int,    # входящие токены
    "tokens_completion": int # исходящие токены
}
```

## Использование

```bash
# OpenAI
python main.py --mode research --model openai --goal "задача"

# Claude (два алиаса)
python main.py --mode research --model anthropic --goal "задача"
python main.py --mode research --model claude --goal "задача"
```

## Skills: путь

```
skills_sistem/agents/SKILL-01_ANALYZER.md  ← универсальный путь
```

Каждый skill-файл содержит MODEL-SPECIFIC RULES внутри.
Orchestrator передаёт MODEL TYPE в system prompt автоматически.

## Переменные окружения

```
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini

ANTHROPIC_API_KEY=...
ANTHROPIC_MODEL=claude-sonnet-4-20250514
```
