#!/bin/bash

# Test script for Anna's [local] Archive
# Verifies that all services are running correctly

set -e

echo "=================================="
echo "Anna's [local] Archive - Test"
echo "=================================="
echo ""

# Determine docker-compose command
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check service health
check_service() {
    local service_name=$1
    local check_command=$2
    
    echo -n "Checking $service_name... "
    if eval "$check_command" &> /dev/null; then
        echo -e "${GREEN}OK${NC}"
        return 0
    else
        echo -e "${RED}FAILED${NC}"
        return 1
    fi
}

# Check if services are running
echo "1. Checking Docker services..."
if ! $DOCKER_COMPOSE ps | grep -q "Up"; then
    echo -e "${RED}Error: Services are not running. Please run './start.sh' first.${NC}"
    exit 1
fi
echo -e "${GREEN}Docker services are running${NC}"
echo ""

# Check MariaDB
echo "2. Checking MariaDB..."
check_service "MariaDB connection" "$DOCKER_COMPOSE exec -T mariadb mysql -uannas -pannas_archive -e 'SELECT 1' 2>/dev/null"
echo ""

# Check Elasticsearch
echo "3. Checking Elasticsearch..."
check_service "Elasticsearch" "curl -s http://localhost:9200/_cluster/health | grep -q '\"status\"'"
echo ""

# Check qBittorrent
echo "4. Checking qBittorrent..."
check_service "qBittorrent Web UI" "curl -s -o /dev/null -w '%{http_code}' http://localhost:8080 | grep -q '200\|401'"
echo ""

# Check Web Application
echo "5. Checking Web Application..."
check_service "Web app health endpoint" "curl -s http://localhost:8000/health | grep -q 'status'"
check_service "Web app home page" "curl -s http://localhost:8000 | grep -q 'Anna'"
echo ""

# Check database tables
echo "6. Checking database schema..."
check_service "local_files table" "$DOCKER_COMPOSE exec -T mariadb mysql -uannas -pannas_archive annas_archive -e 'DESCRIBE local_files' 2>/dev/null"
check_service "archive_offsets table" "$DOCKER_COMPOSE exec -T mariadb mysql -uannas -pannas_archive annas_archive -e 'DESCRIBE archive_offsets' 2>/dev/null"
echo ""

echo "=================================="
echo -e "${GREEN}All tests passed!${NC}"
echo "=================================="
echo ""
echo "Your Anna's [local] Archive is ready to use!"
echo ""
echo "Access points:"
echo "  🌐 Web Interface: http://localhost:8000"
echo "  📦 Torrent Client: http://localhost:8080"
echo ""
