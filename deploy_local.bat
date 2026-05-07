@echo off
REM BBSUL Student Portal - Local Windows Deployment Script
echo === BBSUL Student Portal - Local Setup ===
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.11+ from python.org
    pause
    exit /b 1
)

echo Found Python...
echo.

REM Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo.

REM Set secret key
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo.
)

REM Initialize database
echo Initializing database...
python -c "from app import init_db; init_db()"
echo.

REM Start server
echo Starting Flask server...
echo.
echo ============================================
echo   BBSUL Student Portal is running!
echo ============================================
echo   URL: http://127.0.0.1:5000
echo   Admin: rishabh@bbsul.edu.pk / abc1234
echo.
echo   Press Ctrl+C to stop the server
echo ============================================
echo.

python run.py
