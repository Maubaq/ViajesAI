# Script PowerShell para configurar archivos .env

Write-Host "Configurando archivos de entorno..." -ForegroundColor Cyan

# Backend .env
if (-not (Test-Path "backend\.env")) {
    Write-Host "Creando backend\.env..." -ForegroundColor Yellow
    @" 
# API Key de Google Gemini
GEMINI_API_KEY=AIzaSyBgtKCWZ7IbPujHbfCuCihRfXW3B3VMsb4

# API Key de Weatherbit (opcional - para clima actual)
# Obtén tu clave gratuita en: https://www.weatherbit.io/
# WEATHERBIT_API_KEY=tu_api_key_aqui

# Access Key de Unsplash (opcional - para fotos del destino)
# Obtén tu clave gratuita en: https://unsplash.com/developers
# UNSPLASH_ACCESS_KEY=tu_access_key_aqui

# Configuración del servidor
PORT=5000
FLASK_DEBUG=True

# Orígenes permitidos para CORS (separados por comas)
ALLOWED_ORIGINS=http://localhost:3000

# Modelo de Gemini
GEMINI_MODEL=gemini-2.0-flash
"@ | Out-File -FilePath "backend\.env" -Encoding utf8
    Write-Host "✅ backend\.env creado" -ForegroundColor Green
} else {
    Write-Host "⚠️  backend\.env ya existe" -ForegroundColor Yellow
}

# Frontend .env.development
if (-not (Test-Path "frontend\.env.development")) {
    Write-Host "Creando frontend\.env.development..." -ForegroundColor Yellow
    @"
REACT_APP_API_URL=http://localhost:5000
"@ | Out-File -FilePath "frontend\.env.development" -Encoding utf8
    Write-Host "✅ frontend\.env.development creado" -ForegroundColor Green
} else {
    Write-Host "⚠️  frontend\.env.development ya existe" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Configuración completada!" -ForegroundColor Green
Write-Host ""
Write-Host "Para producción, edita estos archivos con tus valores:" -ForegroundColor Cyan
Write-Host "  - backend\.env (cambia FLASK_DEBUG=False y ALLOWED_ORIGINS)"
Write-Host "  - frontend\.env.production (cambia REACT_APP_API_URL)"

