@echo off
echo ========================================
echo   Therapist Companion Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo ✅ pip found

REM Create virtual environment
echo.
echo 🔧 Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created

REM Activate virtual environment
echo.
echo 🚀 Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated

REM Upgrade pip
echo.
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo 📦 Installing requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    echo Please check requirements.txt and try again
    pause
    exit /b 1
)

echo ✅ Requirements installed successfully

REM Create assets directory if it doesn't exist
if not exist "assets" (
    echo.
    echo 📁 Creating assets directory...
    mkdir assets
    echo ⚠️  Please place your therapist expression images in the 'assets' directory
    echo    Required files: neutral.jpeg, smiling.jpeg, concerned.jpeg, etc.
)

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo 🔑 Creating .env file...
    echo API=YOUR_GOOGLE_GEMINI_API_KEY_HERE > .env
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file and add your Google Gemini API key
    echo    You can get an API key from: https://makersuite.google.com/app/apikey
    echo.
) else (
    echo ✅ .env file already exists
)

echo.
echo ========================================
echo   Setup Complete! 🎉
echo ========================================
echo.
echo To run the application:
echo   1. Make sure you've added your API key to .env file
echo   2. Run: venv\Scripts\python.exe main.py
echo.
echo To build executable for distribution:
echo   Run: venv\Scripts\python.exe build_executable.py
echo.
echo For deployment options, see: DEPLOYMENT.md
echo.
pause