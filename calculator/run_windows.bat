@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
 start "ATLAS Super Calculator" "http://localhost:8765"
 py -3 -m http.server 8765 --bind 127.0.0.1
) else (
 where python >nul 2>nul
 if %errorlevel%==0 (
  start "ATLAS Super Calculator" "http://localhost:8765"
  python -m http.server 8765 --bind 127.0.0.1
 ) else (
  echo Python 3 is required for the local web server.
  echo Install Python or serve this folder with any local HTTP server.
  pause
 )
)
