@echo off
setlocal

REM Paths
set BASE_DIR=C:\Users\hocke\Documents\GitHub\Pokemon-DNS-DS-Server
set STUNNEL_EXE="C:\Program Files (x86)\stunnel\bin\stunnel.exe"
set STUNNEL_CONF=%BASE_DIR%\stunnel\stunnel.conf

REM Start DNS Server
start "DNS Server" cmd /c "cd /d %BASE_DIR% && python dnsserver.py"

REM Start Flask Server
start "Flask Server" cmd /c "cd /d %BASE_DIR% && python server.py"

REM Start stunnel
start "stunnel" %STUNNEL_EXE% %STUNNEL_CONF%

echo.
echo Servers are running. Close this window to stop them all.
echo.

REM Wait until user closes window
pause >nul

REM Kill services
taskkill /IM python.exe /F >nul 2>&1
taskkill /IM stunnel.exe /F >nul 2>&1

echo All services stopped.
