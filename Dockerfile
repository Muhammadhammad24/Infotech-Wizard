# Use Python 3.11 slim image for better performance and security
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TRANSFORMERS_CACHE=/app/.cache/huggingface \
    HF_HOME=/app/.cache/huggingface \
    TORCH_HOME=/app/.cache/torch

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt  

# Copy application code
COPY . .

# Create directories and set permissions
RUN mkdir -p data logs .cache/huggingface .cache/torch

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set ownership for all directories
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Pre-create cache directories with correct permissions
RUN mkdir -p /app/.cache/huggingface/transformers \
             /app/.cache/huggingface/hub \
             /app/.cache/torch

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]