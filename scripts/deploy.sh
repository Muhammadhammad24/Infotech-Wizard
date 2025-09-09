#!/bin/bash

# Deployment script for IT Support Chatbot API
# Usage: ./scripts/deploy.sh [production|development]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
ENVIRONMENT=${1:-development}
IMAGE_NAME="chatbot-backend"
CONTAINER_NAME="it-support-chatbot-api"

echo -e "${BLUE}🚀 Starting deployment for ${ENVIRONMENT} environment...${NC}"

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Error: Docker is not running. Please start Docker and try again.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker is running${NC}"
}

# Function to check if data files exist
check_data_files() {
    echo -e "${YELLOW}🔍 Checking required data files...${NC}"
    
    DATA_DIR="./data"
    REQUIRED_FILES=(
        "it_support_faiss_index.bin"
        "it_support_metadata.pkl"
        "it_support_config.json"
    )
    
    if [ ! -d "$DATA_DIR" ]; then
        echo -e "${YELLOW}⚠️  Warning: Data directory not found. Creating it...${NC}"
        mkdir -p "$DATA_DIR"
    fi
    
    MISSING_FILES=()
    for file in "${REQUIRED_FILES[@]}"; do
        if [ ! -f "$DATA_DIR/$file" ]; then
            MISSING_FILES+=("$file")
        fi
    done
    
    if [ ${#MISSING_FILES[@]} -ne 0 ]; then
        echo -e "${YELLOW}⚠️  Warning: Missing data files:${NC}"
        for file in "${MISSING_FILES[@]}"; do
            echo -e "${YELLOW}   - $DATA_DIR/$file${NC}"
        done
        echo -e "${YELLOW}   The API may not work properly without these files.${NC}"
        echo -e "${YELLOW}   Continue anyway? (y/N)${NC}"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            echo -e "${RED}❌ Deployment cancelled.${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✅ All required data files found${NC}"
    fi
}

# Function to stop existing containers
stop_existing() {
    echo -e "${YELLOW}🛑 Stopping existing containers...${NC}"
    
    if docker ps -q --filter "name=$CONTAINER_NAME" | grep -q .; then
        docker stop "$CONTAINER_NAME"
        echo -e "${GREEN}✅ Stopped existing container: $CONTAINER_NAME${NC}"
    fi
    
    if docker ps -aq --filter "name=$CONTAINER_NAME" | grep -q .; then
        docker rm "$CONTAINER_NAME"
        echo -e "${GREEN}✅ Removed existing container: $CONTAINER_NAME${NC}"
    fi
}

# Function to build Docker image
build_image() {
    echo -e "${BLUE}🔨 Building Docker image...${NC}"
    
    # Build with build args for optimization
    docker build \
        --tag "$IMAGE_NAME:latest" \
        --tag "$IMAGE_NAME:$(date +%Y%m%d-%H%M%S)" \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        .
    
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
}

# Function to deploy with Docker Compose
deploy_compose() {
    echo -e "${BLUE}🐳 Deploying with Docker Compose...${NC}"
    
    # Set environment-specific variables
    if [ "$ENVIRONMENT" = "production" ]; then
        export DEBUG=false
        export LOG_LEVEL=INFO
        export WORKERS=4
    else
        export DEBUG=true
        export LOG_LEVEL=DEBUG
        export WORKERS=1
    fi
    
    # Deploy using docker-compose
    docker-compose up -d
    
    echo -e "${GREEN}✅ Deployment completed${NC}"
}

# Function to run simple Docker deployment
deploy_simple() {
    echo -e "${BLUE}🐳 Deploying with simple Docker run...${NC}"
    
    # Set environment variables
    ENV_VARS=""
    if [ "$ENVIRONMENT" = "production" ]; then
        ENV_VARS="-e DEBUG=false -e LOG_LEVEL=INFO -e WORKERS=4"
    else
        ENV_VARS="-e DEBUG=true -e LOG_LEVEL=DEBUG -e WORKERS=1"
    fi
    
    # Run container
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p 8000:8000 \
        -v "$(pwd)/data:/app/data:ro" \
        -v "$(pwd)/logs:/app/logs" \
        $ENV_VARS \
        --restart unless-stopped \
        "$IMAGE_NAME:latest"
    
    echo -e "${GREEN}✅ Container started successfully${NC}"
}

# Function to show deployment status
show_status() {
    echo -e "${BLUE}📊 Deployment Status:${NC}"
    echo -e "${BLUE}====================${NC}"
    
    # Show container status
    if docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -q "$CONTAINER_NAME"; then
        echo -e "${GREEN}✅ Container is running:${NC}"
        docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    else
        echo -e "${RED}❌ Container is not running${NC}"
        return 1
    fi
    
    echo ""
    echo -e "${BLUE}🔗 API Endpoints:${NC}"
    echo -e "   Health Check: ${GREEN}http://localhost:8000/health${NC}"
    echo -e "   API Documentation: ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "   Chat Endpoint: ${GREEN}http://localhost:8000/api/v1/chat/${NC}"
    
    echo ""
    echo -e "${BLUE}📝 View logs:${NC}"
    echo -e "   docker logs -f $CONTAINER_NAME"
    
    echo ""
    echo -e "${BLUE}🧪 Test the API:${NC}"
    echo -e "   curl http://localhost:8000/health"
}

# Function to test the deployment
test_deployment() {
    echo -e "${YELLOW}🧪 Testing deployment...${NC}"
    
    # Wait a moment for the container to fully start
    sleep 5
    
    # Test health endpoint
    if curl -f -s http://localhost:8000/health > /dev/null; then
        echo -e "${GREEN}✅ Health check passed${NC}"
    else
        echo -e "${RED}❌ Health check failed${NC}"
        echo -e "${YELLOW}Container logs:${NC}"
        docker logs --tail 20 "$CONTAINER_NAME"
        return 1
    fi
}

# Main deployment workflow
main() {
    echo -e "${BLUE}🚀 IT Support Chatbot API Deployment${NC}"
    echo -e "${BLUE}====================================${NC}"
    echo -e "Environment: ${GREEN}$ENVIRONMENT${NC}"
    echo -e "Image: ${GREEN}$IMAGE_NAME${NC}"
    echo -e "Container: ${GREEN}$CONTAINER_NAME${NC}"
    echo ""
    
    # Run deployment steps
    check_docker
    check_data_files
    stop_existing
    build_image
    
    # Choose deployment method
    if [ -f "docker-compose.yml" ]; then
        deploy_compose
    else
        deploy_simple
    fi
    
    # Show status and test
    sleep 3
    show_status
    test_deployment
    
    echo ""
    echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
    echo -e "${BLUE}Your API is now running at: ${GREEN}http://localhost:8000${NC}"
}

# Run main function
main