# Script para iniciar el frontend de ViajeIA
Write-Host "Iniciando frontend de ViajeIA..." -ForegroundColor Cyan

# Navegar a la carpeta frontend
Set-Location -Path "frontend"

# Verificar que .env.development existe
if (-not (Test-Path ".env.development")) {
    Write-Host "Creando archivo .env.development..." -ForegroundColor Yellow
    $envContent = "REACT_APP_API_URL=http://localhost:5000"
    $envContent | Out-File -FilePath ".env.development" -Encoding utf8
    Write-Host "Archivo .env.development creado" -ForegroundColor Green
}

# Verificar que node_modules existe
if (-not (Test-Path "node_modules")) {
    Write-Host "Instalando dependencias de Node.js..." -ForegroundColor Yellow
    npm install
}

# Iniciar servidor de desarrollo
Write-Host ""
Write-Host "Iniciando servidor de desarrollo en http://localhost:3000" -ForegroundColor Green
Write-Host "El navegador se abrira automaticamente" -ForegroundColor Yellow
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

npm start

