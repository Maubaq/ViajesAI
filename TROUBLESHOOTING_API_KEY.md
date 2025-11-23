# 🔧 Troubleshooting: Error 403 - API Key Leaked

## ✅ Verificación: Frontend NO tiene API Keys

El frontend está correctamente configurado:
- ✅ No hay API keys hardcodeadas en el código
- ✅ Solo usa `REACT_APP_API_URL` para hacer peticiones al backend
- ✅ La API key de Gemini solo se usa en las funciones serverless (backend)

## 🔍 Pasos de Troubleshooting

### 1. Verificar Variable de Entorno en Vercel

1. Ve a **Vercel Dashboard** → Tu proyecto → **Settings** → **Environment Variables**
2. Busca `GEMINI_API_KEY`
3. Verifica que el valor sea: `AIzaSyBgtKCWZ7IbPujHbfCuCihRfXW3B3VMsb4`
4. Asegúrate de que esté marcada para **All Environments** (Production, Preview, Development)
5. Si acabas de cambiarla, haz clic en **Save**

### 2. Forzar Nuevo Deployment

Después de actualizar la variable de entorno:

1. Ve a **Deployments**
2. Haz clic en **Redeploy** en el último deployment
3. O mejor aún, haz un pequeño cambio y haz push a GitHub para forzar un nuevo deployment

### 3. Verificar Logs de Funciones Serverless

1. Ve a **Deployments** → Selecciona el último deployment
2. Haz clic en la pestaña **Functions**
3. Busca `/api/planificar`
4. Haz clic en la función para ver los logs
5. Busca errores relacionados con:
   - `GEMINI_API_KEY not found`
   - `API key was reported as leaked`
   - `403` o `401` errors

### 4. Verificar que la Función Recibe la Variable

En los logs de la función, deberías ver que:
- La función se ejecuta correctamente
- No hay errores de "variable not found"
- Si hay un error 403, significa que la API key está llegando pero Google la rechaza

### 5. Probar la API Key Directamente

Si el error persiste, verifica que la nueva API key funcione:

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Verifica que la API key `AIzaSyBgtKCWZ7IbPujHbfCuCihRfXW3B3VMsb4` esté activa
3. Si está bloqueada o reportada como leaked, necesitarás crear una nueva

### 6. Crear Nueva API Key (si es necesario)

Si la API key sigue siendo rechazada:

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una nueva API key
3. Actualiza la variable `GEMINI_API_KEY` en Vercel con la nueva key
4. Redeploy el proyecto

## 🐛 Errores Comunes

### Error: "Your API key was reported as leaked"

**Causa:** La API key fue expuesta públicamente (por ejemplo, en GitHub, documentación, etc.)

**Solución:**
1. Crear una nueva API key en Google AI Studio
2. Actualizar en Vercel
3. **IMPORTANTE:** Asegúrate de que la nueva key NO esté en ningún archivo público
4. Verifica que `.gitignore` excluya archivos `.env`

### Error: "GEMINI_API_KEY not found"

**Causa:** La variable de entorno no está configurada en Vercel

**Solución:**
1. Ve a Vercel → Settings → Environment Variables
2. Agrega `GEMINI_API_KEY` con tu API key
3. Marca para "All Environments"
4. Guarda y redeploy

### Error: 500 Internal Server Error

**Causa:** Error en la función serverless

**Solución:**
1. Revisa los logs de la función en Vercel
2. Verifica que `api/requirements.txt` tenga todas las dependencias
3. Verifica que la función tenga la estructura correcta

## ✅ Checklist de Verificación

- [ ] API key actualizada en Vercel Dashboard
- [ ] Variable marcada para "All Environments"
- [ ] Nuevo deployment realizado después de actualizar
- [ ] Logs de funciones revisados
- [ ] API key verificada en Google AI Studio
- [ ] No hay API keys en archivos públicos (GitHub)
- [ ] `.gitignore` excluye archivos `.env`

## 📝 Notas Importantes

1. **Nunca subas API keys a GitHub** - Están en `.gitignore` pero verifica que no estén en commits anteriores
2. **Las API keys solo se usan en el backend** - El frontend nunca debe tener acceso directo
3. **Usa variables de entorno siempre** - Nunca hardcodees API keys en el código
4. **Rota las keys regularmente** - Si una key fue expuesta, créala nueva inmediatamente

## 🔒 Seguridad

- ✅ Frontend no tiene API keys (correcto)
- ✅ API keys solo en variables de entorno de Vercel (correcto)
- ✅ Funciones serverless leen desde `os.environ.get('GEMINI_API_KEY')` (correcto)
- ⚠️ Verifica que no haya keys en el historial de Git

