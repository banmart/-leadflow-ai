@echo off
echo ========================================
echo LeadFlow AI - Master Setup Script
echo ========================================
echo.
echo This will:
echo  1. Install Python dependencies
echo  2. Guide you through Twitter API setup
echo  3. Launch your marketing campaign
echo  4. Enable automated posting
echo.
pause

echo.
echo [1/4] Installing Python dependencies...
python -m pip install tweepy python-dotenv --quiet

if not exist .env (
    echo.
    echo [2/4] Setting up environment...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit .env and add your Twitter API credentials
    echo.
    echo Open: TWITTER-API-SETUP.md for step-by-step guide
    echo.
    pause
    notepad TWITTER-API-SETUP.md
    echo.
    echo After getting your API keys, paste them into .env
    pause
    notepad .env
)

echo.
echo [3/4] Testing Twitter connection...
python twitter_bot.py post "🤖 BangBot is online! Testing automation for @leadsflowbot"

if %errorlevel% equ 0 (
    echo.
    echo ✅ Twitter connection successful!
    echo.
    echo [4/4] Ready to launch?
    echo.
    set /p launch="Launch LeadFlow AI campaign now? (Y/N): "
    if /i "%launch%"=="Y" (
        python launch_campaign.py all
        echo.
        echo Setting up automated posting...
        call setup_twitter_automation.bat
        echo.
        echo ========================================
        echo 🚀 LAUNCH COMPLETE!
        echo ========================================
        echo.
        echo ✅ Launch thread posted
        echo ✅ Week 1 content scheduled
        echo ✅ Auto-posting enabled (hourly)
        echo.
        echo Check: https://twitter.com/leadsflowbot
        echo.
        echo Next steps:
        echo  - Monitor mentions and engagement
        echo  - Reply to comments
        echo  - Share with your network
        echo.
        echo BangBot will handle the rest! 🤖
    )
) else (
    echo.
    echo ❌ Twitter connection failed
    echo.
    echo Check:
    echo  1. API credentials in .env file
    echo  2. Read & Write permissions enabled
    echo  3. TWITTER-API-SETUP.md for troubleshooting
)

echo.
pause
