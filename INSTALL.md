# 🚀 Guía Rápida de Instalación - ViajeIA

## Instalación en Localhost (Desarrollo)

### Requisitos
- Python 3.8+
- Node.js 16+ y npm
- Git

---

## Paso 1: Backend

```bash
# 1. Navegar a la carpeta backend
cd backend

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
# El archivo .env ya está creado con la API key
# Si necesitas cambiarlo, edita backend/.env

# 6. Ejecutar servidor
python app.py
```

✅ El backend estará en: `http://localhost:5000`

---

## Paso 2: Frontend

Abre una **nueva terminal** (mantén el backend corriendo):

```bash
# 1. Navegar a la carpeta frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Ejecutar aplicación
npm start
```

✅ El frontend se abrirá automáticamente en: `http://localhost:3000`

---

## ✅ Verificar que Funciona

1. Abre `http://localhost:3000` en tu navegador
2. Escribe una pregunta sobre viajes (ej: "¿Qué lugares visitar en París?")
3. Presiona "Planificar mi viaje"
4. Deberías ver la respuesta de Gemini

---

## 🔧 Solución de Problemas

### Error: "Module not found"
```bash
# Backend
cd backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Error: "Port 5000 already in use"
```bash
# Cambia el puerto en backend/.env
PORT=5001
```

### Error: "Cannot connect to API"
- Verifica que el backend esté corriendo en otra terminal
- Verifica que la URL en `frontend/.env.development` sea correcta
- Revisa la consola del navegador para ver errores

### Error: "GEMINI_API_KEY not found"
- Verifica que el archivo `backend/.env` existe
- Verifica que contiene: `GEMINI_API_KEY=AIzaSyDBWWxyQAgBnxFrhxoKGJhS2NTD_MDdnno`

---

## 📝 Notas Importante

- **Mantén ambas terminales abiertas**: una para el backend y otra para el frontend
- **No cierres el servidor backend** mientras uses la aplicación
- El archivo `.env` contiene tu API key - **nunca lo subas a Git** (ya está en .gitignore)

---

## 🎉 ¡Listo!

Tu aplicación está funcionando en localhost. Para desplegarla en producción, consulta `DEPLOYMENT.md`.

