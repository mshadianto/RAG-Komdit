#!/bin/bash
# Startup Script for RAG Komite Audit System
# Runs both backend and frontend in separate processes

echo "======================================"
echo "Starting RAG Komite Audit System"
echo "======================================"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please run setup.sh first and configure your .env file"
    exit 1
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Create log directory
mkdir -p logs

# Start backend in background
echo "🚀 Starting backend server..."
python -m backend.main > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"
echo "   Logs: logs/backend.log"
echo "   URL: http://localhost:8000"
echo ""

# Wait for backend to start
echo "⏳ Waiting for backend to be ready..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "⚠️  Backend health check failed, but continuing..."
fi
echo ""

# Start frontend
echo "🚀 Starting frontend..."
echo "   URL: http://localhost:8501"
echo ""
streamlit run frontend/app.py

# Cleanup when frontend exits
echo ""
echo "Shutting down..."
kill $BACKEND_PID 2>/dev/null
echo "✅ Backend stopped"
echo "👋 Goodbye!"
