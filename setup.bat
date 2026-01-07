@echo off
REM Quick Setup Script for RAG Komite Audit System - Windows
REM Run this script to setup the application quickly

echo ======================================
echo RAG Komite Audit System - Quick Setup
echo ======================================
echo.

REM Check Python version
echo Checking Python version...
python --version 2>nul
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)
echo Python version check passed
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Download embedding model
echo Downloading embedding model...
echo This may take a few minutes on first run...
python -c "from sentence_transformers import SentenceTransformer; print('Downloading...'); model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2'); print('Model downloaded successfully')"
echo.

REM Create .env file if not exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo .env file created
    echo.
    echo ========================================
    echo IMPORTANT: Please edit .env file with your credentials:
    echo    - GROQ_API_KEY (get from https://console.groq.com)
    echo    - SUPABASE_URL (from your Supabase project)
    echo    - SUPABASE_KEY (from your Supabase project)
    echo    - SUPABASE_SERVICE_KEY (from your Supabase project)
    echo ========================================
    echo.
) else (
    echo .env file already exists
    echo.
)

REM Create necessary directories
echo Creating data directories...
if not exist "data\uploads" mkdir data\uploads
if not exist "data\processed" mkdir data\processed
echo Data directories created
echo.

echo ======================================
echo Setup completed successfully!
echo ======================================
echo.
echo Next steps:
echo 1. Edit .env file with your credentials
echo 2. Setup Supabase database:
echo    - Create new project at https://supabase.com
echo    - Run config/database_schema.sql in SQL Editor
echo 3. Start the application:
echo    Backend:  python -m backend.main
echo    Frontend: streamlit run frontend/app.py
echo.
echo For detailed instructions, see README.md
echo.
pause
