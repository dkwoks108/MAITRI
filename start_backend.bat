@echo off
REM MAITRI Backend Startup Script for Windows

echo ==================================
echo MAITRI Backend Startup
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Navigate to backend directory
cd /d "%~dp0backend"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\.installed" (
    echo Installing dependencies...
    echo This may take several minutes on first run...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo. > venv\.installed
    echo Dependencies installed
    echo.
)

REM Check if .env exists
if not exist ".env" (
    echo Creating .env from template...
    copy .env.example .env
    echo .env created
    echo.
)

REM Create data directories
if not exist "data\sessions" mkdir data\sessions
if not exist "data\alerts" mkdir data\alerts

echo Starting MAITRI backend server...
echo API will be available at: http://localhost:8000
echo Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python main.py
