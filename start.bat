@echo off
REM Anna's [local] Archive - Quick Start Script for Windows
REM This script helps you set up and run Anna's [local] Archive

echo ==================================
echo Anna's [local] Archive Setup
echo ==================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed.
    echo Please install Docker Desktop from https://docs.docker.com/desktop/windows/install/
    pause
    exit /b 1
)

echo [OK] Docker is installed

REM Check if Docker daemon is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker daemon is not running.
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [OK] Docker daemon is running
echo.

REM Try docker-compose first, then docker compose
docker-compose version >nul 2>&1
if errorlevel 1 (
    docker compose version >nul 2>&1
    if errorlevel 1 (
        echo Error: Docker Compose is not available.
        echo Please ensure Docker Desktop is properly installed.
        pause
        exit /b 1
    )
    set DOCKER_COMPOSE=docker compose
) else (
    set DOCKER_COMPOSE=docker-compose
)

echo [OK] Docker Compose is available
echo.

REM Build and start services
echo Building and starting services...
echo This may take a few minutes on first run.
echo.

%DOCKER_COMPOSE% up -d --build

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo Services are starting up. This may take a minute...
echo.
echo Access your local archive at:
echo   Web Interface: http://localtest.me:8000
echo   Torrent Client: http://localtest.me:8080
echo.
echo You can also use:
echo   Web Interface: http://localhost:8000
echo   Torrent Client: http://localhost:8080
echo.
echo To check service status:
echo   %DOCKER_COMPOSE% ps
echo.
echo To view logs:
echo   %DOCKER_COMPOSE% logs -f webapp
echo.
echo To stop services:
echo   %DOCKER_COMPOSE% down
echo.
echo For more information, see README.md
echo.
pause
