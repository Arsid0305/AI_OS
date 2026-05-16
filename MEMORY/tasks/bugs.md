# Bugs

_(открытые баги — удалять запись после фикса)_

## Формат
```
## [дата] Краткое название
**Проблема:** ...
**Файл:** path/to/file:line
**Статус:** open / in progress
```

---

## [2026-05-13] openai==2.24.0 не существует
**Проблема:** Версия 2.x OpenAI Python SDK не существует. `pip install -r requirements.txt` падает.
**Файл:** `requirements.txt:4`
**Статус:** open

## [2026-05-13] CORS misconfiguration в WB_BOT — CLOSED
**Проблема:** `allow_origins=["*"]` + `allow_credentials=True` — браузер блокирует fetch-запросы.
**Файл:** `projects/WB_BOT/web/app.py:24`
**Статус:** closed (исправлено в коде)

## [2026-05-13] Захардкоженный бренд "Arols" в подписи
**Проблема:** `SIGNATURE = "команда Arols"` добавляется в каждый ответ, игнорируя настройки бренда.
**Файл:** `projects/WB_BOT/web/app.py:42`
**Статус:** open
