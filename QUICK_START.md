# ⚡ Inicio Rápido - ViajeIA

## Para Probar en Localhost

### 🚀 Opción Más Fácil: Todo en Uno

**Windows (PowerShell):**
```powershell
.\start-all.ps1
```

Este comando iniciará automáticamente:
- ✅ Backend en `http://localhost:5000` (nueva ventana)
- ✅ Frontend en `http://localhost:3000` (nueva ventana)
- ✅ El navegador se abrirá automáticamente

¡Listo! Ya puedes usar la aplicación.

---

### Opción 2: Iniciar por Separado

#### 1️⃣ Iniciar Backend

**Windows (PowerShell):**
```powershell
.\start-backend.ps1
```

**O manualmente:**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

✅ Backend corriendo en: `http://localhost:5000`

> 💡 **Nota:** El script `start-backend.ps1` crea automáticamente el archivo `.env` si no existe y verifica las dependencias.

#### 2️⃣ Iniciar Frontend (Nueva Terminal)

**Windows (PowerShell):**
```powershell
.\start-frontend.ps1
```

**O manualmente:**
```bash
cd frontend
npm install
npm start
```

✅ Frontend abierto en: `http://localhost:3000`

### 4️⃣ ¡Probar!

1. Abre `http://localhost:3000`
2. Escribe una pregunta sobre viajes
3. Presiona "Planificar mi viaje"
4. ¡Disfruta la respuesta de Gemini!

---

## Para Desplegar en Producción

Consulta **[DEPLOYMENT.md](DEPLOYMENT.md)** para la guía completa.

Resumen rápido:
1. Configura servidor Linux
2. Instala dependencias (Python, Node, Nginx)
3. Configura variables de entorno de producción
4. Construye frontend: `npm run build`
5. Configura Gunicorn + Systemd
6. Configura Nginx + SSL
7. ¡Listo!

---

## 🔐 Seguridad Implementada

- ✅ API Key en variables de entorno
- ✅ Rate limiting (10 req/min por IP)
- ✅ Validación de inputs
- ✅ Headers de seguridad
- ✅ CORS configurado
- ✅ Manejo seguro de errores

---

## 📝 Archivos Importantes

- `INSTALL.md` - Instalación detallada
- `DEPLOYMENT.md` - Despliegue en producción
- `backend/.env` - Variables de entorno del backend
- `frontend/.env.development` - Variables de entorno del frontend

---

## ❓ Problemas Comunes

**Error: "GEMINI_API_KEY not found"**
→ Ejecuta el script de setup o crea `backend/.env` manualmente

**Error: "Cannot connect to API" o "ERR_CONNECTION_REFUSED"**
→ El backend no está corriendo. Ejecuta `.\start-backend.ps1` en una terminal separada
→ Verifica que el backend esté en `http://localhost:5000`
→ Asegúrate de que el archivo `backend/.env` existe

**Error: "Port already in use"**
→ Cambia el puerto en `backend/.env` (PORT=5001)

