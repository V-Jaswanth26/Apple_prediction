#!/bin/bash

# Apple Stock Prediction - Deployment Script
# This script handles deployment for different environments

ENVIRONMENT=${1:-development}
echo "Deploying to $ENVIRONMENT environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Backup existing data if it exists
if [ -d "data" ] && [ "$(ls -A data)" ]; then
    echo "Backing up existing data..."
    mkdir -p backups
    tar -czf "backup-$(date +%Y%m%d-%H%M%S).tar.gz" data/
fi

# Build and deploy based on environment
case $ENVIRONMENT in
    "development")
        echo "Starting development environment..."
        docker-compose -f docker-compose.yml up --build
        ;;
    "production")
        echo "Starting production environment..."
        # Set production environment variables
        export FLASK_ENV=production
        export NODE_ENV=production
        
        # Build and deploy
        docker-compose -f docker-compose.yml up --build -d
        
        echo "Production deployment complete!"
        echo "Application is running in detached mode."
        ;;
    "test")
        echo "Starting test environment..."
        # Set test environment variables
        export FLASK_ENV=testing
        export NODE_ENV=test
        
        # Run tests before deployment
        echo "Running tests..."
        cd backend && python -m pytest ../tests/ -v
        cd ../frontend && npm test
        
        # Deploy if tests pass
        docker-compose -f docker-compose.yml up --build
        ;;
    *)
        echo "Unknown environment: $ENVIRONMENT"
        echo "Usage: ./deploy.sh [development|production|test]"
        exit 1
        ;;
esac

echo "Deployment complete!"
