@echo off
REM Startup Script for RAG Komite Audit System - Windows
REM Runs both backend and frontend

echo ======================================
echo Starting RAG Komite Audit System
echo ======================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo Error: .env file not found!
    echo Please run setup.bat first and configure your .env file
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Create log directory
if not exist "logs" mkdir logs

REM Start backend in new window
echo Starting backend server...
start "RAG Backend" cmd /c "python -m backend.main > logs\backend.log 2>&1"
echo Backend started
echo    Logs: logs\backend.log
echo    URL: http://localhost:8000
echo.

REM Wait for backend to start
echo Waiting for backend to be ready...
timeout /t 5 /nobreak > nul
echo.

REM Start frontend
echo Starting frontend...
echo    URL: http://localhost:8501
echo.
streamlit run frontend/app.py

echo.
echo Goodbye!
pause
