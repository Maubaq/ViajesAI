# ViajeIA - Tu Asistente Personal de Viajes

Aplicación web moderna para planificación de viajes con arquitectura de frontend y backend separados.

## Estructura del Proyecto

```
ViajeIA/
├── frontend/          # Aplicación React
│   ├── public/
│   ├── src/
│   └── package.json
└── backend/           # API Flask (Python)
    ├── app.py
    └── requirements.txt
```

## Tecnologías

- **Frontend**: React 18
- **Backend**: Flask (Python)
- **IA**: Google Gemini 2.0 Flash
- **Clima**: Weatherbit API (opcional)
- **Fotos**: Unsplash API (opcional)
- **Estilos**: CSS moderno con gradientes verdes, azules y blancos

## 🚀 Inicio Rápido

### ⚡ Opción Más Fácil: Iniciar Todo Automáticamente

**Windows (PowerShell):**
```powershell
.\start-all.ps1
```

Este script iniciará automáticamente:
- ✅ Backend en `http://localhost:5000` (nueva ventana)
- ✅ Frontend en `http://localhost:3000` (nueva ventana)
- ✅ El navegador se abrirá automáticamente

### Opción 2: Iniciar por Separado

**Terminal 1 - Backend:**
```powershell
.\start-backend.ps1
```

**Terminal 2 - Frontend:**
```powershell
.\start-frontend.ps1
```

### Opción 3: Configuración Manual

**Windows (PowerShell):**
```powershell
.\setup-env.ps1
```

**Linux/Mac:**
```bash
chmod +x setup-env.sh
./setup-env.sh
```

Luego sigue los pasos de instalación abajo.

### Opción 2: Configuración Manual

Crea los archivos de entorno manualmente:

**backend/.env:**
```env
GEMINI_API_KEY=AIzaSyDBWWxyQAgBnxFrhxoKGJhS2NTD_MDdnno
PORT=5000
FLASK_DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
```

**frontend/.env.development:**
```env
REACT_APP_API_URL=http://localhost:5000
```

## 📦 Instalación y Uso

### Backend

1. **Navega a la carpeta backend:**
```bash
cd backend
```

2. **Crea un entorno virtual:**
```bash
python -m venv venv
```

3. **Activa el entorno virtual:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

5. **Configura las variables de entorno:**
   - Ejecuta el script de setup, o
   - Crea `backend/.env` manualmente (ver arriba)

6. **Ejecuta el servidor:**

**Opción fácil (Windows):**
```powershell
# Desde la raíz del proyecto
.\start-backend.ps1
```

**O manualmente:**
```bash
python app.py
```

✅ El backend estará disponible en `http://localhost:5000`

### Frontend

1. **Navega a la carpeta frontend:**
```bash
cd frontend
```

2. **Instala las dependencias:**
```bash
npm install
```

3. **Configura las variables de entorno:**
   - El script de setup ya lo hace, o
   - Crea `frontend/.env.development` manualmente (ver arriba)

4. **Ejecuta la aplicación:**
```bash
npm start
```

✅ El frontend estará disponible en `http://localhost:3000`

> 📖 **Para instrucciones detalladas, consulta [INSTALL.md](INSTALL.md)**

## Características

- ✅ Interfaz moderna y profesional
- ✅ Campo de texto para preguntas sobre viajes
- ✅ Botón "Planificar mi viaje" con estados de carga
- ✅ Integración con Google Gemini Pro para respuestas inteligentes
- ✅ Área de respuestas dinámica con animaciones
- ✅ Manejo de errores mejorado
- ✅ Diseño responsive
- ✅ Colores: verdes, azules y blancos
- ✅ UX optimizada con feedback visual

## Funcionalidades de UX

- **Estados de carga**: Animaciones mientras se procesa la solicitud
- **Manejo de errores**: Mensajes claros cuando algo falla
- **Botón de limpiar**: Fácil limpieza del formulario
- **Animaciones suaves**: Transiciones fluidas para mejor experiencia
- **Feedback visual**: Indicadores claros del estado de la aplicación

## 🔒 Seguridad

- ✅ API Key almacenada en variables de entorno (no en código)
- ✅ Rate limiting implementado
- ✅ Validación y sanitización de inputs
- ✅ Headers de seguridad configurados
- ✅ CORS configurado para producción
- ✅ Manejo seguro de errores

## 🌐 Despliegue en Producción

Para desplegar en un servidor con dominio, consulta la guía completa:
**[DEPLOYMENT.md](DEPLOYMENT.md)**

Incluye:
- Configuración de servidor Linux
- Nginx reverse proxy
- SSL con Let's Encrypt
- Gunicorn para producción
- Systemd service
- Buenas prácticas de seguridad

## 📚 Documentación

- **[INSTALL.md](INSTALL.md)** - Guía rápida de instalación en localhost
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía completa de despliegue en producción
- **[WEATHERBIT_SETUP.md](WEATHERBIT_SETUP.md)** - Configuración de Weatherbit API para clima actual
- **[UNSPLASH_SETUP.md](UNSPLASH_SETUP.md)** - Configuración de Unsplash API para fotos del destino

## Próximos Pasos

- Agregar historial de conversaciones
- Implementar autenticación de usuarios
- Agregar más funcionalidades de planificación de viajes
- Guardar conversaciones en base de datos

