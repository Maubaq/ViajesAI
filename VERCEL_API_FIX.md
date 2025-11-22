# 🔧 Solución: Error 405 en API Routes

## Problema

Cuando Root Directory está configurado como `frontend`, Vercel busca las funciones serverless en la raíz del proyecto (no dentro de `frontend`). El error 405 (Method Not Allowed) indica que las rutas API no están siendo enrutadas correctamente.

## Solución

### Opción 1: Mover funciones API a la raíz (Recomendado)

Si Root Directory = `frontend`, las funciones serverless deben estar en la raíz del proyecto:
```
ViajeIA/
├── api/              # Funciones serverless (en la raíz)
│   ├── planificar.py
│   ├── health.py
│   └── requirements.txt
└── frontend/          # Root Directory
    ├── src/
    └── package.json
```

### Opción 2: Cambiar Root Directory a vacío

Si prefieres mantener la estructura actual:
1. En Vercel Dashboard → Settings → General
2. Cambia **Root Directory** a vacío (sin valor)
3. Actualiza `vercel.json`:
```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/build",
  "installCommand": "cd frontend && npm install"
}
```

## Verificación

1. Las funciones en `api/` deben tener la clase `handler` exportada
2. El archivo debe terminar con la clase `handler` (ya está correcto)
3. Las variables de entorno deben estar configuradas en Vercel:
   - `GEMINI_API_KEY`
   - `GEMINI_MODEL`
   - `WEATHERBIT_API_KEY` (opcional)
   - `UNSPLASH_ACCESS_KEY` (opcional)

## Debugging

Si sigue fallando, verifica en Vercel Dashboard:
- **Functions** tab → Deberías ver `api/planificar` y `api/health`
- **Logs** → Revisa los logs de las funciones para ver errores específicos

