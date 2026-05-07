# Deployment Script for Windows
# Run this in PowerShell as Administrator

Write-Host "=== BBSUL Student Portal Deployment ===" -ForegroundColor Green

# Check Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker is installed" -ForegroundColor Green

# Create .env if doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env file created. Please edit .env to set your SECRET_KEY" -ForegroundColor Green
}

# Build image
Write-Host ""
Write-Host "Building Docker image..." -ForegroundColor Cyan
docker-compose build

# Start services
Write-Host ""
Write-Host "Starting services..." -ForegroundColor Cyan
docker-compose up -d

# Wait for health check
Write-Host ""
Write-Host "Waiting for application to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Show status
Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Application URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "👤 Admin Login: rishabh@bbsul.edu.pk" -ForegroundColor Cyan
Write-Host "🔑 Admin Password: abc1234" -ForegroundColor Cyan
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f web" -ForegroundColor White
Write-Host ""
Write-Host "To stop:" -ForegroundColor Yellow
Write-Host "  docker-compose down" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANT: Change the SECRET_KEY in .env file!" -ForegroundColor Red
