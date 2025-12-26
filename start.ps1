# LLM Council - Start script for PowerShell
Write-Host "Starting LLM Council..." -ForegroundColor Cyan
Write-Host ""

# Start backend
Write-Host "Starting backend on http://localhost:8001..." -ForegroundColor Green
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    uv run python -m backend.main
}

# Wait a bit for backend to start
Start-Sleep -Seconds 2

# Start frontend
Write-Host "Starting frontend on http://localhost:5173..." -ForegroundColor Green
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "$using:PWD\frontend"
    npm run dev
}

Write-Host ""
Write-Host "LLM Council is running!" -ForegroundColor Green
Write-Host "  Backend:  http://localhost:8001"
Write-Host "  Frontend: http://localhost:5173"
Write-Host ""
Write-Host "Press Ctrl+C to stop both servers" -ForegroundColor Yellow

# Cleanup function
function Stop-Services {
    Write-Host "`nStopping services..." -ForegroundColor Yellow
    Stop-Job -Job $backendJob -ErrorAction SilentlyContinue
    Stop-Job -Job $frontendJob -ErrorAction SilentlyContinue
    Remove-Job -Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job -Job $frontendJob -ErrorAction SilentlyContinue
    Write-Host "Services stopped." -ForegroundColor Green
}

# Handle Ctrl+C
try {
    # Monitor jobs and display output
    while ($true) {
        # Check if jobs are still running
        $backendState = (Get-Job -Id $backendJob.Id).State
        $frontendState = (Get-Job -Id $frontendJob.Id).State
        
        if ($backendState -eq "Failed" -or $frontendState -eq "Failed") {
            Write-Host "One or more services failed. Check logs above." -ForegroundColor Red
            break
        }
        
        # Receive output from jobs
        Receive-Job -Job $backendJob -ErrorAction SilentlyContinue
        Receive-Job -Job $frontendJob -ErrorAction SilentlyContinue
        
        Start-Sleep -Milliseconds 500
    }
}
finally {
    Stop-Services
}
