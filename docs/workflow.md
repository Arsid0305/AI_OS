# Полный цикл работы (кратко)

Каждый раз:

```bash
# 1. Перейти в папку runtime
cd C:\DATA\AI_OS\runtime

# 2. Активировать виртуальное окружение
venv\Scripts\activate

# 3. Запустить сервер
python -m uvicorn web.app:app --reload
```

Должно появиться: `Uvicorn running on http://127.0.0.1:8000`

Сервер НЕ закрывать.

Открыть браузер: `http://127.0.0.1:8000`

Остановить сервер: `Ctrl + C`
