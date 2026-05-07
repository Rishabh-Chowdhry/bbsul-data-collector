#!/bin/bash
# Deployment script for BBSUL Student Portal

echo "=== BBSUL Student Portal Deployment ==="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please edit .env to set your SECRET_KEY"
fi

# Build and start services
echo ""
echo "Building Docker image..."
docker-compose build

echo ""
echo "Starting services..."
docker-compose up -d

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Application URL: http://localhost:5000"
echo "👤 Admin Login: rishabh@bbsul.edu.pk"
echo "🔑 Admin Password: abc1234"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f web"
echo ""
echo "To stop:"
echo "  docker-compose down"
echo ""
echo "⚠️  Please change the SECRET_KEY in .env file for production!"
