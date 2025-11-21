# 🔧 Solución Definitiva para Vercel - Error de Build

## ⚠️ Problema Actual

El build está fallando porque Vercel no está detectando correctamente la estructura del proyecto.

## ✅ Solución: Configuración Manual en Vercel Dashboard

**IMPORTANTE:** Necesitas configurar manualmente en el dashboard de Vercel, NO solo con `vercel.json`.

### Paso 1: Ir a Settings del Proyecto

1. Ve a https://vercel.com/dashboard
2. Selecciona tu proyecto `ViajesAI`
3. Haz clic en **Settings** (arriba)
4. Ve a la sección **General**

### Paso 2: Configurar Build Settings

En la sección **Build & Development Settings**, configura:

```
Framework Preset: Create React App
Root Directory: frontend
Build Command: npm run build
Output Directory: build
Install Command: npm install
```

**Pasos detallados:**
1. Haz clic en **"Override"** o **"Edit"** en cada campo
2. **Root Directory:** Escribe `frontend` (sin barra al final)
3. **Build Command:** `npm run build`
4. **Output Directory:** `build`
5. **Install Command:** `npm install`
6. Haz clic en **Save**

### Paso 3: Verificar Variables de Entorno

Ve a **Settings → Environment Variables** y asegúrate de tener:

```
GEMINI_API_KEY=AIzaSyDBWWxyQAgBnxFrhxoKGJhS2NTD_MDdnno
GEMINI_MODEL=gemini-2.0-flash
WEATHERBIT_API_KEY=dbc51eb5faf3451da9f8855daf663c06
UNSPLASH_ACCESS_KEY=tu_key_aqui
```

**IMPORTANTE:** Marca todas para **Production**, **Preview** y **Development**.

### Paso 4: Hacer Push de los Cambios

```powershell
git add .
git commit -m "Simplify vercel.json - use manual config"
git push origin main
```

### Paso 5: Forzar Nuevo Despliegue

1. En Vercel Dashboard, ve a **Deployments**
2. Haz clic en los **tres puntos (⋯)** del último deployment
3. Selecciona **"Redeploy"**
4. Espera a que termine el build

### Paso 6: Después del Despliegue Exitoso

Una vez que el build sea exitoso:

1. Obtendrás una URL como: `viajes-ia-git-main-maubaqs-projects.vercel.app`
2. Ve a **Settings → Environment Variables**
3. Agrega:
   ```
   REACT_APP_API_URL=https://viajes-ia-git-main-maubaqs-projects.vercel.app
   ```
   (Reemplaza con tu URL real)
4. Vercel hará un nuevo despliegue automáticamente

---

## 🔍 Verificar Logs de Build

Si sigue fallando:

1. Ve a **Deployments** en Vercel
2. Haz clic en el deployment fallido
3. Ve a la pestaña **"Logs"**
4. Revisa el error completo
5. Comparte el error conmigo para ayudarte mejor

---

## 📋 Checklist

- [ ] Root Directory configurado como `frontend` en Vercel Dashboard
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `build`
- [ ] Install Command: `npm install`
- [ ] Variables de entorno configuradas
- [ ] Cambios subidos a GitHub (`git push`)
- [ ] Nuevo despliegue iniciado en Vercel

---

## 💡 Nota Importante

El archivo `vercel.json` ahora está simplificado. Vercel usará la configuración manual del dashboard, que es más confiable para proyectos con estructura de subcarpetas.

