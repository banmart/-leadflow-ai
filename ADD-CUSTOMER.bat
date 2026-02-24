@echo off
chcp 65001 >nul
cd C:\Users\banma\.openclaw\workspace\projects\leadflow-ai

echo ========================================
echo  LeadFlow AI - Add New Customer
echo ========================================
echo.

set /p name="Customer Name: "
set /p email="Email: "

echo.
echo Choose Plan:
echo   1 = Starter ($149/mo)
echo   2 = Growth ($299/mo)
echo   3 = Agency ($499/mo)
echo.
set /p plan_num="Enter 1, 2, or 3: "

if "%plan_num%"=="1" set plan=starter
if "%plan_num%"=="2" set plan=growth
if "%plan_num%"=="3" set plan=agency

echo.
echo Processing signup...
set PYTHONIOENCODING=utf-8
python automate_onboarding.py signup "%name%" %email% %plan%

echo.
echo ========================================
echo DONE! They got welcome email.
echo ========================================
echo.
echo When they PAY, run: ACTIVATE-CUSTOMER.bat
echo.
pause
