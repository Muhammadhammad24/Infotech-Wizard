#!/bin/bash

# Docker entrypoint script for IT Support Chatbot API
# This script handles initialization and startup tasks

set -e

echo "🚀 Starting IT Support Chatbot API..."

# Print environment info
echo "📊 Environment Information:"
echo "  - Python version: $(python --version)"
echo "  - Working directory: $(pwd)"
echo "  - User: $(whoami)"
echo "  - Available memory: $(free -h | grep '^Mem:' | awk '{print $2}' || echo 'N/A')"

# Check if data directory exists and has required files
echo "🔍 Checking data files..."
DATA_DIR="/app/data"

if [ ! -d "$DATA_DIR" ]; then
    echo "⚠️  Warning: Data directory not found at $DATA_DIR"
    echo "   Creating directory..."
    mkdir -p "$DATA_DIR"
else
    echo "✅ Data directory found"
fi

# Check for required FAISS files
FAISS_INDEX="${FAISS_INDEX_PATH:-/app/data/it_support_faiss_index.bin}"
METADATA_FILE="${METADATA_PATH:-/app/data/it_support_metadata.pkl}"
CONFIG_FILE="${CONFIG_PATH:-/app/data/it_support_config.json}"

if [ ! -f "$FAISS_INDEX" ]; then
    echo "⚠️  Warning: FAISS index file not found at $FAISS_INDEX"
    echo "   The API may not work properly without this file."
else
    echo "✅ FAISS index file found: $FAISS_INDEX"
fi

if [ ! -f "$METADATA_FILE" ]; then
    echo "⚠️  Warning: Metadata file not found at $METADATA_FILE"
else
    echo "✅ Metadata file found: $METADATA_FILE"
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo "⚠️  Warning: Config file not found at $CONFIG_FILE"
else
    echo "✅ Config file found: $CONFIG_FILE"
fi

# Pre-download models if in production mode
if [ "${DEBUG:-true}" = "false" ]; then
    echo "🤖 Pre-warming models in production mode..."
    python -c "
import os
os.environ['PYTHONPATH'] = '/app'
try:
    from app.services.embeddings import EmbeddingService
    print('📥 Loading embedding model...')
    emb = EmbeddingService()
    print('✅ Embedding model loaded successfully')
except Exception as e:
    print(f'⚠️  Warning: Could not pre-load embedding model: {e}')

try:
    from app.services.chatbot import ChatbotService
    print('🧠 Initializing chatbot service...')
    chatbot = ChatbotService()
    if chatbot.is_ready():
        print('✅ Chatbot service ready')
    else:
        print('⚠️  Warning: Chatbot service not fully ready')
except Exception as e:
    print(f'⚠️  Warning: Could not initialize chatbot service: {e}')
"
else
    echo "🔧 Running in debug mode - skipping model pre-warming"
fi

# Create logs directory if it doesn't exist
LOGS_DIR="/app/logs"
if [ ! -d "$LOGS_DIR" ]; then
    echo "📝 Creating logs directory..."
    mkdir -p "$LOGS_DIR"
    chmod 755 "$LOGS_DIR"
fi

echo "🌟 Initialization complete!"
echo "🚀 Starting FastAPI server..."
echo "   - Host: ${HOST:-0.0.0.0}"
echo "   - Port: ${PORT:-8000}"
echo "   - Workers: ${WORKERS:-1}"
echo "   - Debug: ${DEBUG:-true}"
echo "   - Log Level: ${LOG_LEVEL:-INFO}"

# Execute the main command
exec "$@"