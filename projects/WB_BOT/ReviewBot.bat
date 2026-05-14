@echo off
chcp 65001 > nul
title ReviewBot WB
color 0A

echo.
echo  ==========================================
echo   ReviewBot WB
echo  ==========================================
echo.

cd /d "%~dp0"

call "%~dp0..\..\runtime\venv\Scripts\activate.bat"

echo  Token check...
python -c "from dotenv import load_dotenv; import os, requests; load_dotenv(dotenv_path=r'%~dp0..\..\runtime\.env'); t=os.getenv('WB_TOKEN','').strip(); r=requests.get('https://feedbacks-api.wildberries.ru/api/v1/feedbacks',headers={'Authorization':f'Bearer {t}'},params={'isAnswered':'false','take':1,'skip':0},timeout=15); print('  Token: OK' if r.status_code==200 else f'  Token: ERROR {r.status_code}')" 2>nul || echo   Token check skipped

echo.
echo  Server: http://127.0.0.1:8000
echo  Stop: Ctrl+C
echo.

start /b timeout /t 2 /nobreak >nul && start "" "%~dp0wb-reviewbot-v3.html"

python -m uvicorn web.app:app --host 127.0.0.1 --port 8000 --env-file "%~dp0..\..\runtime\.env"

pause
