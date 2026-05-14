# AI OS

Персональная операционная система для работы с любым AI-инструментом.

> Единое ядро правил, скиллов и памяти — для Claude, ChatGPT, Cursor, Gemini и Codex.

---

## Что это

AI OS — это прослойка между вами и любым AI-инструментом. Вместо того чтобы переписывать инструкции под каждый инструмент заново, вы определяете правила один раз — в `SYSTEM.md` — а каждый AI подключается через свой адаптер.

### Архитектура

```
SYSTEM.md          ← универсальное ядро (читается любым AI)
CLAUDE.md          ← адаптер для Claude Code
ADAPTERS/          ← адаптеры для ChatGPT, Gemini, Codex, Claude Web
skills_sistem/     ← 8 скиллов (ANALYZER, WRITER, RESEARCHER и др.)
MEMORY/            ← память: баги, задачи, решения, уроки
runtime/           ← Python CLI для запуска агентов через OpenAI / Anthropic
docs/              ← документация, тесты, памятка
```

---

## Поддерживаемые AI-инструменты

| Инструмент | Подключение |
|---|---|
| Claude Code | автоматически через `CLAUDE.md` |
| Cursor | автоматически через `.cursor/rules/ai-os.mdc` |
| Codex | автоматически (читает весь репо) |
| Claude Web | вставить `SYSTEM.md` + `ADAPTERS/claude-web/BOOTSTRAP.md` |
| ChatGPT | вставить `SYSTEM.md` + `ADAPTERS/chatgpt/BOOTSTRAP.md` |
| Gemini | вставить `SYSTEM.md` + `ADAPTERS/gemini/GEMINI.md` |

---

## Быстрый старт

### 1. Клонировать репо

```bash
git clone https://github.com/arsid0305/ai_os.git
cd ai_os
```

### 2. Создать виртуальное окружение

```bash
cd runtime
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r ../requirements.txt
```

### 4. Создать `.env`

```bash
cp .env.example .env
# Открыть .env и ввести ключи
```

Нужные переменные:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...   # опционально
```

---

## Запуск через CLI

```bash
cd runtime
python main.py --mode research --goal "Как работает рынок Wildberries"
```

### Доступные режимы

| Режим | Назначение |
|---|---|
| `research` | Глубокий анализ темы |
| `code` | Написать / отладить код |
| `review` | Критический ревью текста или кода |
| `decision` | Анализ решения, варианты, риски |
| `legal` | Анализ документов (РФ) |
| `medical` | Разбор медицинских документов |
| `marketplace` | Анализ продукта на маркетплейсе |
| `tables` | Формулы для Excel / Google Sheets |
| `writing` | Написать / отредактировать текст |
| `visual` | Промпты для генерации изображений |
| `meta_agent` | Проектирование AI-агентов |
| `meta_prompt` | Генерация системных промптов |

### Параметры

```bash
--mode      режим работы (обязателен)
--goal      задача / запрос (обязателен)
--model     openai или anthropic (default: openai)
--output    сохранить результат в файл
--project   сохранить в папку проекта
```

### Примеры

```bash
# Исследование через Anthropic
python main.py --mode research --model anthropic --goal "Тренды e-commerce 2025"

# Код и сохранение в файл
python main.py --mode code --goal "Напиши CRUD для FastAPI" -o result.md

# Анализ договора
python main.py --mode legal --goal "Текст договора..."
```

---

## Скиллы

Система автоматически выбирает скилл под задачу. Вы можете указать скилл явно в начале запроса или в проектных инструкциях.

| Скилл | Назначение |
|---|---|
| BOOTSTRAP | Стартовый режим |
| ANALYZER | Анализ, выводы |
| VALIDATOR | Проверка по критериям |
| PLANNER | Планирование и риски |
| OPERATOR | Исполнение (low risk) |
| WRITER | Тексты и документы |
| RESEARCHER | Сбор и синтез информации |
| CRITIC | Оппонент идей |

Подробно: `skills_sistem/SKILLS_ALL.md`

---

## Структура проекта

```
ai_os/
├── SYSTEM.md                  ← универсальное ядро
├── CLAUDE.md                  ← адаптер Claude Code
├── requirements.txt
├── ADAPTERS/
│   ├── chatgpt/BOOTSTRAP.md
│   ├── claude-web/BOOTSTRAP.md
│   ├── codex/BOOTSTRAP.md
│   └── gemini/GEMINI.md
├── MEMORY/
│   ├── tasks/
│   │   ├── bugs.md
│   │   ├── todo.md
│   │   └── decisions.md
│   └── lessons/lessons.md
├── skills_sistem/
│   ├── agents/SKILL-0X_*.md
│   └── SKILLS_ALL.md
├── runtime/
│   ├── main.py                    ← CLI запуск
│   ├── core/                      ← оркестратор, память, протоколы
│   ├── engine/                    ← движки OpenAI и Anthropic
│   └── prompts/                   ← 12 режимов (v1.json + domain.md)
├── docs/
│   ├── ARCHITECTURE.md            ← архитектура системы
│   ├── AI_TESTING.md              ← инструкция по тестированию AI
│   ├── ai_benchmark.md            ← результаты тестов (прогоны)
│   └── памятка.md                 ← памятка по работе с AI_OS
└── projects/
    └── WB_BOT/                    ← бот для ответов на Wildberries / Ozon
```

---

## Лицензия

MIT
