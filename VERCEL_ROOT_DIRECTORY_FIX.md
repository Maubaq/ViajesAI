# 🔧 Solución: Root Directory configurado como `frontend`

## Problema

Cuando configuras **Root Directory** como `frontend` en Vercel, el sistema ya está trabajando desde dentro del directorio `frontend`. Por lo tanto, los comandos NO deben incluir `cd frontend`.

## Configuración Correcta

### En Vercel Dashboard:
- **Root Directory:** `frontend` ✅
- **Build Command:** `npm install && npm run build` (sin `cd frontend`)
- **Output Directory:** `build` (sin `frontend/`)
- **Install Command:** `npm install` (sin `cd frontend`)

### En vercel.json:
El archivo `vercel.json` ahora está configurado para trabajar con Root Directory = `frontend`:
- Los comandos NO incluyen `cd frontend`
- El `outputDirectory` es `build` (relativo al Root Directory)
- Las rutas API usan `/../api/$1` para salir del directorio `frontend` y acceder a `api/`

## Importante

Si cambias el Root Directory a vacío (raíz del proyecto), necesitarás actualizar `vercel.json` para incluir `cd frontend` en los comandos.

