@echo off
chcp 65001 >nul
cd C:\Users\banma\.openclaw\workspace\projects\leadflow-ai

echo ========================================
echo  LeadFlow AI - Activate Paid Customer
echo ========================================
echo.

set /p email="Customer Email: "

echo.
echo Activating customer...
set PYTHONIOENCODING=utf-8
python automate_onboarding.py paid %email%

echo.
echo ========================================
echo ACTIVATION COMPLETE!
echo ========================================
echo.
echo Now add them to send_leads_email.py
echo (Copy the info shown above)
echo.
echo They get leads tomorrow at 8 AM!
echo.
pause
