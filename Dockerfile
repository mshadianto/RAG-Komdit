# Use Python slim image
FROM python:3.10-slim

# Cache buster - change this to force rebuild
ARG CACHE_BUST=20260109v3

# Set working directory
WORKDIR /app

# Set Python path early
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install CPU-only PyTorch first (much smaller ~200MB vs 2GB)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copy only backend-related code (not frontend)
COPY backend/ ./backend/
COPY agents/ ./agents/
COPY config/ ./config/

# Expose port
EXPOSE 8000

# Start command
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
