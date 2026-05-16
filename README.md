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
.cursor/rules/     ← адаптер для Cursor
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

---

## Скиллы

Система автоматически выбирает скилл под задачу.

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

---

## Лицензия

MIT
