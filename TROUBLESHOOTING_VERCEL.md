# 🔧 Troubleshooting: Errores de Build en Vercel

## Problema 1: Errores de ESLint

### Error:
```
Failed to compile.
Line 84:56: Unnecessary escape character: \` no-useless-escape
Line 104:56: Unnecessary escape character: \" no-useless-escape
Line 440:39: Unnecessary escape character: \` no-useless-escape
Line 441:25: 'contenido' is assigned a value but never used no-unused-vars
Line 441:57: Unnecessary escape character: \` no-useless-escape
Line 442:75: Unnecessary escape character: \` no-useless-escape
```

### Solución:
✅ **Corregido en el código:**
- Removidos escapes innecesarios en expresiones regulares: `[•\-\*]` → `[•\-*]`
- Eliminada variable `contenido` no utilizada en línea 441
- Los escapes de `\` dentro de `[]` en regex no son necesarios

### Verificación:
- Los errores de ESLint han sido corregidos
- El build debería completarse sin errores de compilación

---

## Problema 2: Discrepancia en Configuración de Vercel

### Error:
Hay una discrepancia entre **Production Overrides** y **Project Settings**:
- **Production Override:** `npm install && npm run build`
- **Project Settings:** `cd frontend && npm run build`

### Solución:

#### Opción A: Sincronizar Project Settings con Production (Recomendado)

1. Ve a **Settings** → **General** → **Build and Development Settings**
2. Asegúrate de que:
   - **Root Directory:** Vacío (sin valor)
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Output Directory:** `frontend/build`
   - **Install Command:** `cd frontend && npm install`
3. Haz clic en **Save**
4. Ve a **Deployments** y haz clic en **Redeploy**

#### Opción B: Usar Production Overrides

Si prefieres usar los Production Overrides:
1. Ve a **Settings** → **General** → **Build and Development Settings**
2. Cambia **Root Directory** a `frontend`
3. Actualiza los comandos:
   - **Build Command:** `npm install && npm run build`
   - **Output Directory:** `build`
   - **Install Command:** `npm install`
4. **IMPORTANTE:** También necesitarás mover o ajustar las funciones API

---

## Problema 3: Error 405 en API Routes

### Error:
```
Failed to load resource: the server responded with a status of 405
/api/planificar:1
```

### Solución:

#### Verificar que las funciones API estén en la ubicación correcta:

Con **Root Directory vacío** (recomendado):
```
ViajeIA/
├── api/              # ✅ Funciones serverless aquí
│   ├── planificar.py
│   ├── health.py
│   └── requirements.txt
└── frontend/         # Frontend React
    ├── src/
    └── package.json
```

#### Verificar estructura de funciones:

Las funciones Python deben tener:
```python
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Tu código aquí
        pass
```

#### Verificar variables de entorno en Vercel:

1. Ve a **Settings** → **Environment Variables**
2. Asegúrate de tener:
   - `GEMINI_API_KEY` (requerido)
   - `GEMINI_MODEL` (opcional, default: gemini-2.0-flash)
   - `WEATHERBIT_API_KEY` (opcional)
   - `UNSPLASH_ACCESS_KEY` (opcional)
3. Marca todas para **Production**, **Preview** y **Development**

#### Verificar logs de funciones:

1. Ve a **Deployments** → Selecciona el deployment
2. Ve a la pestaña **Functions**
3. Revisa los logs de `/api/planificar` y `/api/health`
4. Busca errores específicos

---

## Checklist de Verificación

### ✅ Configuración de Build:
- [ ] Root Directory está vacío (o configurado correctamente)
- [ ] Build Command: `cd frontend && npm install && npm run build`
- [ ] Output Directory: `frontend/build`
- [ ] Install Command: `cd frontend && npm install`

### ✅ Funciones API:
- [ ] Archivos en `api/` están en la raíz del proyecto
- [ ] Cada función tiene la clase `handler` exportada
- [ ] `requirements.txt` tiene todas las dependencias

### ✅ Variables de Entorno:
- [ ] `GEMINI_API_KEY` configurada
- [ ] Variables marcadas para todos los entornos
- [ ] Valores correctos (sin espacios extra)

### ✅ Código:
- [ ] Sin errores de ESLint
- [ ] Sin variables no utilizadas
- [ ] Sin escapes innecesarios en regex

---

## Pasos de Resolución Rápida

1. **Corregir errores de ESLint** ✅ (Ya hecho)
2. **Sincronizar configuración de Vercel:**
   - Root Directory: Vacío
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/build`
3. **Verificar variables de entorno**
4. **Redeploy en Vercel**
5. **Probar endpoints API:**
   - `https://tu-dominio.vercel.app/api/health` (debe retornar 200)
   - `https://tu-dominio.vercel.app/api/planificar` (debe aceptar POST)

---

## Comandos Útiles para Debugging

### Ver logs de build:
En Vercel Dashboard → Deployments → Selecciona deployment → Build Logs

### Ver logs de funciones:
En Vercel Dashboard → Deployments → Selecciona deployment → Functions → Click en función → Logs

### Probar API localmente:
```bash
# Instalar dependencias de API
cd api
pip install -r requirements.txt

# Probar función (requiere configuración especial para Vercel)
```

---

## Contacto y Soporte

Si después de seguir estos pasos el problema persiste:
1. Revisa los logs completos en Vercel
2. Verifica que todas las variables de entorno estén correctas
3. Asegúrate de que el commit más reciente esté desplegado

