@echo off
chcp 65001 > nul
cd /d "%~dp0"

set PORT=5000
set LOCKFILE=%TEMP%\harussukssuk.lock

if exist "%LOCKFILE%" del "%LOCKFILE%" > nul 2>&1

echo 하루쑥쑥 서버를 중지합니다...
py -c "import os, subprocess, signal; [os.kill(int(p.split(',')[1]), signal.SIGTERM) for p in subprocess.check_output(['tasklist','/FI','IMAGENAME eq python.exe','/FO','CSV']).decode('cp949',errors='ignore').strip().split(chr(10))[1:] if 'run.py' in p]; [os.kill(int(p.split(',')[1]), signal.SIGTERM) for p in subprocess.check_output(['tasklist','/FI','IMAGENAME eq pythonw.exe','/FO','CSV']).decode('cp949',errors='ignore').strip().split(chr(10))[1:] if 'run.py' in p]" 2> nul

timeout /t 2 /nobreak > nul
echo 완료. 창을 닫으셔도 됩니다.
timeout /t 3 /nobreak > nul
