# LLM Council - Simple Start Script for PowerShell
# This version runs processes in separate windows for better visibility

Write-Host "Starting LLM Council..." -ForegroundColor Cyan
Write-Host ""

# Start backend in a new PowerShell window
Write-Host "Starting backend on http://localhost:8001..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; Write-Host 'Backend Server' -ForegroundColor Cyan; uv run python -m backend.main"

# Wait a bit for backend to start
Start-Sleep -Seconds 2

# Start frontend in a new PowerShell window
Write-Host "Starting frontend on http://localhost:5173..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; Write-Host 'Frontend Server' -ForegroundColor Cyan; npm run dev"

Write-Host ""
Write-Host "LLM Council is starting!" -ForegroundColor Green
Write-Host "  Backend:  http://localhost:8001"
Write-Host "  Frontend: http://localhost:5173"
Write-Host ""
Write-Host "Both servers are running in separate windows." -ForegroundColor Yellow
Write-Host "Close those windows to stop the servers." -ForegroundColor Yellow
