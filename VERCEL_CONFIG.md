# ⚠️ Configuración Importante para Vercel

## Problema: Root Directory

Si Vercel sigue dando el error `ENOENT: no such file or directory, open '/vercel/path0/package.json'`, necesitas configurar el **Root Directory** en el dashboard de Vercel.

## Solución: Configurar Root Directory en Vercel Dashboard

1. Ve a tu proyecto en [vercel.com](https://vercel.com)
2. Haz clic en **Settings** (Configuración)
3. Ve a la sección **General**
4. Busca **Root Directory**
5. **Déjalo en blanco** (no pongas nada) - esto hará que Vercel use la raíz del repositorio
6. Guarda los cambios
7. Vuelve a desplegar

## Alternativa: Si quieres usar `frontend` como Root Directory

Si prefieres configurar `frontend` como Root Directory:

1. En **Settings** → **General** → **Root Directory**
2. Escribe: `frontend`
3. Guarda los cambios
4. **IMPORTANTE**: Actualiza `vercel.json` para que las rutas API funcionen correctamente:

```json
{
  "buildCommand": "npm install && npm run build",
  "outputDirectory": "build",
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/../api/$1"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

## Recomendación

**Usa la raíz del repositorio** (Root Directory vacío) y mantén la configuración actual de `vercel.json`. Esto es más simple y funciona mejor con la estructura actual del proyecto.

