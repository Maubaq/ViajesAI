#!/bin/bash
# Script para configurar archivos .env

echo "Configurando archivos de entorno..."

# Backend .env
if [ ! -f backend/.env ]; then
    echo "Creando backend/.env..."
    cat > backend/.env << EOF
# API Key de Google Gemini
GEMINI_API_KEY=AIzaSyBgtKCWZ7IbPujHbfCuCihRfXW3B3VMsb4

# Configuración del servidor
PORT=5000
FLASK_DEBUG=True

# Orígenes permitidos para CORS (separados por comas)
ALLOWED_ORIGINS=http://localhost:3000
EOF
    echo "✅ backend/.env creado"
else
    echo "⚠️  backend/.env ya existe"
fi

# Frontend .env.development
if [ ! -f frontend/.env.development ]; then
    echo "Creando frontend/.env.development..."
    cat > frontend/.env.development << EOF
REACT_APP_API_URL=http://localhost:5000
EOF
    echo "✅ frontend/.env.development creado"
else
    echo "⚠️  frontend/.env.development ya existe"
fi

echo ""
echo "✅ Configuración completada!"
echo ""
echo "Para producción, edita estos archivos con tus valores:"
echo "  - backend/.env (cambia FLASK_DEBUG=False y ALLOWED_ORIGINS)"
echo "  - frontend/.env.production (cambia REACT_APP_API_URL)"

