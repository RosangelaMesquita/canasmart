@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo [INFO] Criando ambiente virtual .venv...
  py -3 -m venv .venv || python -m venv .venv
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
echo.
pause
