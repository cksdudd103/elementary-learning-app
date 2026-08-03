@echo off
chcp 65001 > nul
cd /d "%~dp0"

set PORT=5000
set LOCKFILE=%TEMP%\harussukssuk.lock

if exist "%LOCKFILE%" (
    start "" http://127.0.0.1:%PORT%/
    exit
)

echo. > "%LOCKFILE%"

py -c "import socket; s=socket.socket(); exit(0 if s.connect_ex(('127.0.0.1', %PORT%)) != 0 else 1)" > nul 2>&1
if %errorlevel% == 0 (
    start /B "" pyw run.py
    timeout /t 4 /nobreak > nul
)

start "" http://127.0.0.1:%PORT%/
exit
