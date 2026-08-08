@echo off
setlocal
cd /d "C:\Users\dell5488\WorkBuddy\2026-08-07-20-44-05"
echo ============================================
echo  Blacklist HTTP Server
echo  iKuai URL: http://192.168.100.52:8899/ikuai_blacklist_hosts.txt
echo  Press Ctrl+C to stop.
echo ============================================
where python >nul 2>&1
if %errorlevel%==0 (
    python -m http.server 8899 --bind 0.0.0.0
) else (
    where py >nul 2>&1
    if %errorlevel%==0 (
        py -m http.server 8899 --bind 0.0.0.0
    ) else (
        echo ERROR: Python not found in PATH.
        pause
    )
)
