@echo off
setlocal

REM Paths
set BASE_DIR=C:\Users\hocke\Documents\GitHub\Pokemon-DNS-DS-Server
set STUNNEL_EXE="C:\Program Files (x86)\stunnel\bin\stunnel.exe"
set STUNNEL_CONF=%BASE_DIR%\wii-wfc-dev\stunnel\stunnel.conf

echo === Starting DNS Server ===
start "DNS Server" cmd /k "cd /d %BASE_DIR% && python dnsserver.py"

echo === Starting Flask Server ===
start "Flask Server" cmd /k "cd /d %BASE_DIR% && python server.py"

echo === Starting stunnel ===
start "stunnel" %STUNNEL_EXE% %STUNNEL_CONF%

echo All services launched!
pause
