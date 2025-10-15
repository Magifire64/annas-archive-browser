#!/bin/bash

# Anna's [local] Archive - Quick Start Script
# This script helps you set up and run Anna's [local] Archive

set -e

echo "=================================="
echo "Anna's [local] Archive Setup"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed."
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "Error: Docker Compose is not installed."
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

# Determine docker-compose command
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

echo "✓ Docker is installed"
echo "✓ Docker Compose is available"
echo ""

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "Error: Docker daemon is not running."
    echo "Please start Docker and try again."
    exit 1
fi

echo "✓ Docker daemon is running"
echo ""

# Build and start services
echo "Building and starting services..."
echo "This may take a few minutes on first run."
echo ""

$DOCKER_COMPOSE up -d --build

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Services are starting up. This may take a minute..."
echo ""
echo "Access your local archive at:"
echo "  🌐 Web Interface: http://localtest.me:8000"
echo "  📦 Torrent Client: http://localtest.me:8080"
echo ""
echo "You can also use:"
echo "  🌐 Web Interface: http://localhost:8000"
echo "  📦 Torrent Client: http://localhost:8080"
echo ""
echo "To check service status:"
echo "  $DOCKER_COMPOSE ps"
echo ""
echo "To view logs:"
echo "  $DOCKER_COMPOSE logs -f webapp"
echo ""
echo "To stop services:"
echo "  $DOCKER_COMPOSE down"
echo ""
echo "For more information, see README.md"
echo ""
