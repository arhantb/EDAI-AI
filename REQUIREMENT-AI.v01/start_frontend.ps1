# REQUIREMENT-AI v0.1 - Frontend Startup Script
# Optimized for Windows PowerShell

Write-Host "🎨 Starting REQUIREMENT-AI Frontend..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Check if requirements are installed
Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow
python -c "import streamlit, plotly, pandas" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies." -ForegroundColor Red
        exit 1
    }
}

# Start the frontend
Write-Host "🌟 Starting Streamlit frontend..." -ForegroundColor Green
Write-Host "🌐 Frontend will open at http://localhost:8501" -ForegroundColor Cyan
Write-Host "📋 Features: Analytics, Validator, Templates, Priority Assistant" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

streamlit run ui/ui_app.py
