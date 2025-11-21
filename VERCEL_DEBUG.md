# 🔍 Debug de Vercel - Identificar el Error

## Pasos para Ver los Logs Completos

1. Ve a **Deployments** en Vercel Dashboard
2. Haz clic en el deployment que falló (el que dice "Build Failed")
3. Haz clic en la pestaña **"Build Logs"** o **"Logs"**
4. Revisa el error completo

## Errores Comunes y Soluciones

### Error 1: "npm ERR! code ENOENT"
**Causa:** No encuentra `package.json`
**Solución:** Verifica que `frontend/package.json` existe en el repositorio

### Error 2: "Module not found" o "Cannot find module"
**Causa:** Dependencias faltantes
**Solución:** Verifica que `frontend/package.json` tiene todas las dependencias

### Error 3: "Build failed" sin detalles
**Causa:** Error en el código de React
**Solución:** Revisa si hay errores de sintaxis en `App.jsx`

### Error 4: "Command exited with 1"
**Causa:** Cualquier error durante el build
**Solución:** Revisa los logs completos para ver el error específico

## Verificar Estructura del Repositorio

Asegúrate de que en GitHub tu repositorio tenga:

```
ViajesAI/
  ├── api/
  │   ├── planificar.py
  │   ├── health.py
  │   └── requirements.txt
  ├── frontend/
  │   ├── package.json      ✅ (debe existir)
  │   ├── src/
  │   └── public/
  └── vercel.json
```

## Comandos para Verificar Localmente

```powershell
# Verificar que package.json existe
Test-Path frontend\package.json

# Probar build localmente
cd frontend
npm install
npm run build
```

Si el build funciona localmente pero falla en Vercel, el problema es de configuración.
Si el build falla localmente también, hay un error en el código.

