@echo off
echo Pushing LeadFlow AI to GitHub...
echo.

cd C:\Users\banma\.openclaw\workspace\projects\leadflow-ai

echo Repository: https://github.com/banmart/leadflow-ai
echo.

git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ======================================
    echo Push failed! Possible reasons:
    echo ======================================
    echo.
    echo 1. Repository doesn't exist yet
    echo    Go to: https://github.com/new
    echo    Name: leadflow-ai
    echo    Click "Create repository"
    echo.
    echo 2. Need to authenticate
    echo    Windows will prompt for credentials
    echo    Or use: GitHub Desktop / VS Code
    echo.
    echo 3. Wrong repository name
    echo    Check: https://github.com/banmart
    echo.
    pause
) else (
    echo.
    echo ✅ Successfully pushed to GitHub!
    echo.
    echo View at: https://github.com/banmart/leadflow-ai
    echo.
    pause
)
