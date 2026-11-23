@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 goto use_py
where python >nul 2>nul
if %errorlevel%==0 goto use_python
echo Python 3 was not found. Install Python or host this folder on GitHub Pages.
pause
exit /b 1
:use_py
start "" "http://127.0.0.1:8000/"
py -3 -m http.server 8000 --bind 127.0.0.1
pause
exit /b
:use_python
start "" "http://127.0.0.1:8000/"
python -m http.server 8000 --bind 127.0.0.1
pause
