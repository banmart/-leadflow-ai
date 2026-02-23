@echo off
echo ========================================
echo LeadFlow AI - Twitter Automation Setup
echo ========================================
echo.

REM Create scheduled task to post queued tweets every hour
schtasks /create /tn "LeadFlowAI-Twitter-Queue" /tr "python C:\Users\banma\.openclaw\workspace\projects\leadflow-ai\twitter_bot.py queue" /sc hourly /st 00:00 /f

if %errorlevel% equ 0 (
    echo.
    echo ✅ Automated posting enabled!
    echo    Windows Task Scheduler will run every hour
    echo    Posts scheduled tweets from twitter_queue.json
    echo.
) else (
    echo.
    echo ❌ Failed to create scheduled task
    echo    Run this script as Administrator
    echo.
)

pause
