# REQUIREMENT-AI v0.1 - Complete Startup Script
# Starts both backend and frontend in separate windows

Write-Host "🚀 Starting REQUIREMENT-AI Complete System..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
}

Write-Host "🌟 Starting Backend in new window..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start_backend.ps1"

Start-Sleep -Seconds 3

Write-Host "🎨 Starting Frontend in new window..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start_frontend.ps1"

Write-Host ""
Write-Host "✅ Both services are starting..." -ForegroundColor Green
Write-Host "🔗 Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "🌐 Frontend: http://localhost:8501" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 New Features Available:" -ForegroundColor Magenta
Write-Host "  📊 Analytics Dashboard" -ForegroundColor White
Write-Host "  ✅ Quick Requirements Validator" -ForegroundColor White
Write-Host "  📝 Template Builder" -ForegroundColor White
Write-Host "  🎯 Priority Assistant" -ForegroundColor White
Write-Host "  ⚡ Performance Monitor" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit this launcher..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
