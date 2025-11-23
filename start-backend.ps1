# Script para iniciar el backend de ViajeIA
Write-Host "Iniciando backend de ViajeIA..." -ForegroundColor Cyan

# Navegar a la carpeta backend
Set-Location -Path "backend"

# Verificar que .env existe y tiene codificación correcta
$envExists = Test-Path ".env"
if (-not $envExists) {
    Write-Host "Creando archivo .env..." -ForegroundColor Yellow
    $envContent = @"
# API Key de Google Gemini
GEMINI_API_KEY=AIzaSyBgtKCWZ7IbPujHbfCuCihRfXW3B3VMsb4

# API Key de Weatherbit (opcional - para clima actual)
# Obtén tu clave gratuita en: https://www.weatherbit.io/
# WEATHERBIT_API_KEY=tu_api_key_aqui

# Access Key de Unsplash (opcional - para fotos del destino)
# Obtén tu clave gratuita en: https://unsplash.com/developers
# UNSPLASH_ACCESS_KEY=tu_access_key_aqui

# Configuracion del servidor
PORT=5000
FLASK_DEBUG=True

# Origenes permitidos para CORS
ALLOWED_ORIGINS=http://localhost:3000

# Modelo de Gemini
GEMINI_MODEL=gemini-2.0-flash
"@
    # Crear con codificación UTF-8 sin BOM
    [System.IO.File]::WriteAllText((Resolve-Path ".").Path + "\.env", $envContent, [System.Text.UTF8Encoding]::new($false))
    Write-Host "Archivo .env creado con codificacion UTF-8" -ForegroundColor Green
} else {
    # Verificar que el archivo se puede leer correctamente
    try {
        $testContent = Get-Content ".env" -Encoding UTF8 -ErrorAction Stop
        Write-Host "Archivo .env verificado" -ForegroundColor Green
    } catch {
        Write-Host "Recreando archivo .env con codificacion correcta..." -ForegroundColor Yellow
        $envContent = @"
# API Key de Google Gemini
GEMINI_API_KEY=AIzaSyBgtKCWZ7IbPujHbfCuCihRfXW3B3VMsb4

# API Key de Weatherbit (opcional - para clima actual)
# Obtén tu clave gratuita en: https://www.weatherbit.io/
# WEATHERBIT_API_KEY=tu_api_key_aqui

# Access Key de Unsplash (opcional - para fotos del destino)
# Obtén tu clave gratuita en: https://unsplash.com/developers
# UNSPLASH_ACCESS_KEY=tu_access_key_aqui

# Configuracion del servidor
PORT=5000
FLASK_DEBUG=True

# Origenes permitidos para CORS
ALLOWED_ORIGINS=http://localhost:3000

# Modelo de Gemini
GEMINI_MODEL=gemini-2.0-flash
"@
        [System.IO.File]::WriteAllText((Resolve-Path ".").Path + "\.env", $envContent, [System.Text.UTF8Encoding]::new($false))
        Write-Host "Archivo .env recreado" -ForegroundColor Green
    }
}

# Activar entorno virtual
if (Test-Path "venv\Scripts\activate.ps1") {
    Write-Host "Activando entorno virtual..." -ForegroundColor Green
    & .\venv\Scripts\activate.ps1
} else {
    Write-Host "Entorno virtual no encontrado. Creando..." -ForegroundColor Red
    python -m venv venv
    & .\venv\Scripts\activate.ps1
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Verificar dependencias
Write-Host "Verificando dependencias..." -ForegroundColor Cyan
python -c "import flask, flask_cors, google.generativeai, dotenv" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Instalando dependencias faltantes..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Iniciar servidor
Write-Host ""
Write-Host "Iniciando servidor en http://localhost:5000" -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

python app.py
