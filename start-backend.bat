@echo off
echo Iniciando backend de ViajeIA...
cd backend

REM Verificar que .env existe
if not exist .env (
    echo Creando archivo .env...
    (
        echo # API Key de Google Gemini
        echo GEMINI_API_KEY=AIzaSyBgtKCWZ7IbPujHbfCuCihRfXW3B3VMsb4
        echo.
        echo # Configuración del servidor
        echo PORT=5000
        echo FLASK_DEBUG=True
        echo.
        echo # Orígenes permitidos para CORS
        echo ALLOWED_ORIGINS=http://localhost:3000
        echo.
        echo # Modelo de Gemini
        echo GEMINI_MODEL=gemini-2.0-flash-exp
    ) > .env
)

REM Activar entorno virtual e iniciar
call venv\Scripts\activate.bat
python app.py
pause

