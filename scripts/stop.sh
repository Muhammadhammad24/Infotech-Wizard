#!/bin/bash

# Stop script for IT Support Chatbot API
# Usage: ./scripts/stop.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

CONTAINER_NAME="it-support-chatbot-api"
COMPOSE_FILE="docker-compose.yml"

echo -e "${BLUE}🛑 Stopping IT Support Chatbot API...${NC}"
echo -e "${BLUE}====================================${NC}"

# Function to stop using Docker Compose if available
stop_with_compose() {
    if [ -f "$COMPOSE_FILE" ]; then
        echo -e "${YELLOW}📄 Found docker-compose.yml, using Docker Compose...${NC}"
        
        # Stop all services
        docker-compose stop
        
        echo -e "${GREEN}✅ Services stopped with Docker Compose${NC}"
        
        # Optional: Remove containers
        echo -e "${YELLOW}❓ Remove containers as well? (y/N)${NC}"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            docker-compose down
            echo -e "${GREEN}✅ Containers removed${NC}"
        fi
        
        return 0
    else
        return 1
    fi
}

# Function to stop using direct Docker commands
stop_with_docker() {
    echo -e "${YELLOW}🐳 Using direct Docker commands...${NC}"
    
    # Check if container exists and is running
    if docker ps -q --filter "name=$CONTAINER_NAME" | grep -q .; then
        echo -e "${YELLOW}🛑 Stopping container: $CONTAINER_NAME${NC}"
        docker stop "$CONTAINER_NAME"
        echo -e "${GREEN}✅ Container stopped: $CONTAINER_NAME${NC}"
    else
        echo -e "${YELLOW}⚠️  Container not running: $CONTAINER_NAME${NC}"
    fi
    
    # Check if container exists (stopped)
    if docker ps -aq --filter "name=$CONTAINER_NAME" | grep -q .; then
        echo -e "${YELLOW}❓ Remove stopped container? (y/N)${NC}"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            docker rm "$CONTAINER_NAME"
            echo -e "${GREEN}✅ Container removed: $CONTAINER_NAME${NC}"
        fi
    fi
}

# Function to show remaining containers and images
show_status() {
    echo -e "${BLUE}📊 Current Status:${NC}"
    echo -e "${BLUE}=================${NC}"
    
    # Show running containers related to our app
    echo -e "${YELLOW}🐳 Running containers:${NC}"
    if docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" | grep -E "(chatbot|it-support)" || true; then
        echo -e "${YELLOW}   (No related containers running)${NC}"
    fi
    
    echo ""
    
    # Show our images
    echo -e "${YELLOW}🖼️  Related images:${NC}"
    docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}" | grep -E "(chatbot|it-support)" || echo -e "${YELLOW}   (No related images found)${NC}"
}

# Function to cleanup everything (optional)
cleanup_all() {
    echo -e "${RED}🗑️  Full cleanup mode${NC}"
    echo -e "${RED}⚠️  This will remove all containers, images, and volumes related to the chatbot${NC}"
    echo -e "${YELLOW}❓ Are you sure? This action cannot be undone. (y/N)${NC}"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        # Stop and remove containers
        docker ps -aq --filter "name=*chatbot*" --filter "name=*it-support*" | xargs -r docker stop
        docker ps -aq --filter "name=*chatbot*" --filter "name=*it-support*" | xargs -r docker rm
        
        # Remove images
        docker images -q "*chatbot*" "*it-support*" | xargs -r docker rmi -f
        
        # Remove Docker Compose volumes if they exist
        if [ -f "$COMPOSE_FILE" ]; then
            docker-compose down -v 2>/dev/null || true
        fi
        
        echo -e "${GREEN}✅ Full cleanup completed${NC}"
    else
        echo -e "${YELLOW}❌ Cleanup cancelled${NC}"
    fi
}

# Main function
main() {
    # Try to stop with Docker Compose first, then fallback to direct Docker
    if ! stop_with_compose; then
        stop_with_docker
    fi
    
    echo ""
    show_status
    
    echo ""
    echo -e "${YELLOW}❓ Perform full cleanup (remove all images and volumes)? (y/N)${NC}"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        cleanup_all
    fi
    
    echo ""
    echo -e "${GREEN}🎉 Stop completed!${NC}"
    
    # Show helpful commands
    echo -e "${BLUE}💡 Helpful commands:${NC}"
    echo -e "   View all containers: ${GREEN}docker ps -a${NC}"
    echo -e "   View all images:     ${GREEN}docker images${NC}"
    echo -e "   Start again:         ${GREEN}./scripts/deploy.sh${NC}"
}

# Run main function
main