@echo off
cd /d "%~dp0"
python main.py || py -3 main.py
echo.
pause
