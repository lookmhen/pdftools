@echo off
cd %~dp0
call "venv\Scripts\activate.bat"
cmd /c "python app.py"

start chrome "https://http://127.0.0.1:5000"

