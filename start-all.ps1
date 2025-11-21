# Script para iniciar backend y frontend de ViajeIA
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ViajeIA - Iniciando Servidores" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "Error: Este script debe ejecutarse desde la raiz del proyecto" -ForegroundColor Red
    exit 1
}

# Iniciar backend en una nueva ventana
Write-Host "Iniciando backend en nueva ventana..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; if (-not (Test-Path '.env')) { @'
GEMINI_API_KEY=AIzaSyDBWWxyQAgBnxFrhxoKGJhS2NTD_MDdnno
PORT=5000
FLASK_DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
GEMINI_MODEL=gemini-2.0-flash
'@ | Out-File -FilePath '.env' -Encoding utf8 }; if (Test-Path 'venv\Scripts\activate.ps1') { .\venv\Scripts\activate.ps1; python app.py } else { python -m venv venv; .\venv\Scripts\activate.ps1; pip install -r requirements.txt; python app.py }"

# Esperar un poco para que el backend inicie
Write-Host "Esperando 3 segundos para que el backend inicie..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Iniciar frontend en otra nueva ventana
Write-Host "Iniciando frontend en nueva ventana..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; if (-not (Test-Path '.env.development')) { 'REACT_APP_API_URL=http://localhost:5000' | Out-File -FilePath '.env.development' -Encoding utf8 }; if (-not (Test-Path 'node_modules')) { npm install }; npm start"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Servidores iniciados!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:5000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "El navegador se abrira automaticamente con el frontend" -ForegroundColor Yellow
Write-Host "Cierra las ventanas de PowerShell para detener los servidores" -ForegroundColor Yellow

