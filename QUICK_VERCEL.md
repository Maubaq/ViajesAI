# ⚡ Guía Rápida - Desplegar ViajeIA en Vercel

## ✅ Lo que NO necesitas hacer

❌ **NO ejecutes `npm run build` manualmente** - Vercel lo hace automáticamente
❌ **NO necesitas construir el backend** - Vercel maneja las funciones serverless
❌ **NO necesitas instalar dependencias en producción** - Vercel lo hace

## 🚀 Pasos para Desplegar

### 1. Preparar Git (si no lo has hecho)

```powershell
# En la raíz del proyecto (C:\Users\mauri\Desktop\APPS AI\ViajeIA)
cd "C:\Users\mauri\Desktop\APPS AI\ViajeIA"

# Si no has inicializado Git
git init
git add .
git commit -m "Ready for Vercel deployment"
```

### 2. Subir a GitHub

1. Ve a [github.com](https://github.com) y crea un nuevo repositorio
2. Conecta tu proyecto local:

```powershell
# Reemplaza TU_USUARIO con tu usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/viajeia.git
git branch -M main
git push -u origin main
```

### 3. Conectar con Vercel

1. Ve a [vercel.com](https://vercel.com) e inicia sesión
2. Haz clic en **"Add New..."** → **"Project"**
3. Selecciona **"Import Git Repository"**
4. Conecta GitHub si es necesario
5. Selecciona el repositorio `viajeia`

### 4. Configurar en Vercel

Vercel detectará automáticamente la configuración desde `vercel.json`. Solo necesitas:

#### 4.1 Configurar el Frontend

- **Framework Preset:** React
- **Root Directory:** `frontend`
- **Build Command:** `npm run build` (ya está configurado)
- **Output Directory:** `build` (ya está configurado)
- **Install Command:** `npm install` (ya está configurado)

#### 4.2 Variables de Entorno

En **Settings** → **Environment Variables**, agrega:

```
GEMINI_API_KEY=AIzaSyBgtKCWZ7IbPujHbfCuCihRfXW3B3VMsb4
GEMINI_MODEL=gemini-2.0-flash
WEATHERBIT_API_KEY=dbc51eb5faf3451da9f8855daf663c06
UNSPLASH_ACCESS_KEY=tu_unsplash_key_aqui
```

**Importante:** Marca todas las variables para **Production**, **Preview** y **Development**.

### 5. Desplegar

1. Haz clic en **"Deploy"**
2. Vercel construirá y desplegará automáticamente
3. Espera 2-3 minutos mientras se construye

### 6. Configurar URL del Frontend (Después del primer despliegue)

Una vez que Vercel termine el despliegue:

1. Obtendrás una URL como: `viajeia-abc123.vercel.app`
2. Ve a **Settings** → **Environment Variables**
3. Agrega:
   ```
   REACT_APP_API_URL=https://viajeia-abc123.vercel.app
   ```
   (Reemplaza con tu URL real)
4. Vercel hará un nuevo despliegue automáticamente

### 7. ¡Listo!

Tu aplicación estará disponible en la URL que Vercel te proporcionó.

---

## 🔧 Comandos Útiles (Solo para Desarrollo Local)

### Frontend (React)
```powershell
cd frontend
npm install    # Solo la primera vez
npm start      # Para desarrollo local
npm run build  # Solo si quieres probar el build localmente
```

### Backend (Python/Flask)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

**Nota:** Para Vercel, NO necesitas ejecutar estos comandos. Vercel lo hace automáticamente.

---

## ❓ Preguntas Frecuentes

### ¿Por qué no funciona `npm run build` en el backend?

El backend es **Python/Flask**, no usa npm. Solo el frontend (React) usa npm.

### ¿Necesito construir el proyecto antes de subirlo a GitHub?

**NO.** Vercel construye todo automáticamente cuando haces push.

### ¿Qué archivos debo subir a GitHub?

Todo excepto:
- `node_modules/` (ya está en .gitignore)
- `venv/` (ya está en .gitignore)
- `.env` (ya está en .gitignore)
- `build/` (ya está en .gitignore)

### ¿Cómo sé si el despliegue fue exitoso?

1. Ve al dashboard de Vercel
2. Verás el estado del despliegue
3. Si hay errores, verás los logs detallados

---

## 🐛 Solución de Problemas

### Error: "Module not found"
- Verifica que `backend/requirements.txt` tenga todas las dependencias
- Verifica que `frontend/package.json` esté correcto

### Error: "Environment variable not found"
- Verifica que todas las variables estén en Vercel
- Asegúrate de que estén marcadas para el entorno correcto

### Error: "Build failed"
- Revisa los logs en Vercel Dashboard
- Verifica que la estructura de carpetas sea correcta

---

## 📝 Checklist Final

- [ ] Proyecto subido a GitHub
- [ ] Vercel conectado con GitHub
- [ ] Variables de entorno configuradas en Vercel
- [ ] Primer despliegue completado
- [ ] `REACT_APP_API_URL` configurada con la URL de Vercel
- [ ] Aplicación funcionando en producción

---

¡Listo! Tu aplicación estará en línea en minutos. 🎉

