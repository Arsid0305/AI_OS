# Полный цикл запуска WB_BOT

```bash
# 1. Активировать venv
cd C:\DATA\AI_OS\runtime
venv\Scripts\activate

# 2. Перейти в папку бота
cd C:\DATA\AI_OS\projects\WB_bot

# 3. Запустить сервер
python -m uvicorn web.app:app --reload
```

Должно появиться: `Uvicorn running on http://127.0.0.1:8000`

Сервер НЕ закрывать.

Открыть браузер: `http://127.0.0.1:8000`

Остановить сервер: `Ctrl + C`
