# ⚠️ IMPORTANTE: Cambiar Root Directory en Vercel

## Problema Actual

Con Root Directory = `frontend`, Vercel no está detectando las funciones serverless en `api/` porque están fuera del Root Directory.

## Solución: Cambiar Root Directory a Vacío

### Pasos en Vercel Dashboard:

1. Ve a tu proyecto en [vercel.com](https://vercel.com)
2. Haz clic en **Settings** (Configuración)
3. Ve a la sección **General**
4. Busca **Root Directory**
5. **BORRA el valor `frontend`** y déjalo completamente vacío
6. Haz clic en **Save**
7. Ve a **Deployments** y haz clic en **Redeploy** en el último deployment

### ¿Por qué?

- Cuando Root Directory está vacío, Vercel usa la raíz del repositorio
- Las funciones serverless en `api/` se detectan automáticamente
- El `vercel.json` ahora tiene comandos con `cd frontend` para construir el frontend
- Las rutas API funcionan correctamente desde la raíz

### Configuración Actualizada

El `vercel.json` ahora está configurado para:
- **Build Command:** `cd frontend && npm install && npm run build`
- **Output Directory:** `frontend/build`
- **Install Command:** `cd frontend && npm install`

Esto funciona cuando Root Directory está vacío (raíz del proyecto).

## Después del Cambio

Una vez que cambies Root Directory a vacío y Vercel redespiegue:
- ✅ Las funciones en `api/` se detectarán automáticamente
- ✅ El frontend se construirá correctamente desde `frontend/`
- ✅ Las rutas `/api/planificar` y `/api/health` funcionarán
- ✅ El error 405 debería desaparecer

