#!/bin/bash
# Quick Setup Script for RAG Komite Audit System
# Run this script to setup the application quickly

echo "======================================"
echo "RAG Komite Audit System - Quick Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Python 3.10 or higher is required. Current version: $python_version"
    exit 1
fi
echo "✅ Python version: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Download embedding model
echo "Downloading embedding model..."
python -c "from sentence_transformers import SentenceTransformer; print('Downloading...'); model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2'); print('✅ Model downloaded successfully')"
echo ""

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your credentials:"
    echo "   - GROQ_API_KEY (get from https://console.groq.com)"
    echo "   - SUPABASE_URL (from your Supabase project)"
    echo "   - SUPABASE_KEY (from your Supabase project)"
    echo "   - SUPABASE_SERVICE_KEY (from your Supabase project)"
    echo ""
else
    echo "ℹ️  .env file already exists"
    echo ""
fi

# Create necessary directories
echo "Creating data directories..."
mkdir -p data/uploads data/processed
echo "✅ Data directories created"
echo ""

echo "======================================"
echo "✅ Setup completed successfully!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Setup Supabase database:"
echo "   - Create new project at https://supabase.com"
echo "   - Run config/database_schema.sql in SQL Editor"
echo "3. Start the application:"
echo "   Backend:  python -m backend.main"
echo "   Frontend: streamlit run frontend/app.py"
echo ""
echo "For detailed instructions, see README.md"
echo ""
