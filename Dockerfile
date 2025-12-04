# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from backend directory
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the backend application
COPY backend/ .

# Create necessary directories
RUN mkdir -p uploads instance

# Expose port
EXPOSE 8000

# Run gunicorn using wsgi.py entry point
CMD exec gunicorn "wsgi:app" --bind 0.0.0.0:${PORT:-8000} --workers 1 --threads 2 --timeout 0
