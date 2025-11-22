# 🚀 Guía de Despliegue en Vercel - ViajeIA

## ✅ Cambios Realizados

1. **vercel.json actualizado**: Configurado para construir el frontend y manejar las rutas API
2. **frontend/src/App.jsx actualizado**: Usa rutas relativas de API en producción
3. **API functions listas**: Las funciones en `api/` están configuradas para Vercel serverless

## 📋 Pasos para Desplegar

### 1. Subir Cambios a GitHub

```powershell
# Agregar los cambios
git add vercel.json frontend/src/App.jsx

# Hacer commit
git commit -m "Configuración para Vercel: actualizado vercel.json y rutas API relativas"

# Subir a GitHub
git push origin main
```

### 2. Conectar con Vercel

1. Ve a [vercel.com](https://vercel.com) e inicia sesión
2. Haz clic en **"Add New..."** → **"Project"**
3. Selecciona **"Import Git Repository"**
4. Conecta tu cuenta de GitHub si es necesario
5. Selecciona el repositorio: **Maubaq/ViajesAI**

### 3. Configurar el Proyecto en Vercel

Vercel detectará automáticamente la configuración. Solo necesitas:

#### Framework Settings:
- **Framework Preset:** Create React App (o React)
- **Root Directory:** `frontend` (o dejar en blanco si Vercel lo detecta)
- **Build Command:** `npm run build` (automático)
- **Output Directory:** `build` (automático)
- **Install Command:** `npm install` (automático)

#### Environment Variables:

Ve a **Settings** → **Environment Variables** y agrega:

```
GEMINI_API_KEY=tu_gemini_api_key_aqui
GEMINI_MODEL=gemini-2.0-flash
WEATHERBIT_API_KEY=tu_weatherbit_key (opcional)
UNSPLASH_ACCESS_KEY=tu_unsplash_key (opcional)
```

**Importante:** 
- Marca todas las variables para **Production**, **Preview** y **Development**
- NO agregues `REACT_APP_API_URL` - el código usa rutas relativas automáticamente

### 4. Desplegar

1. Haz clic en **"Deploy"**
2. Vercel construirá y desplegará automáticamente
3. Espera 2-3 minutos mientras se construye

### 5. Verificar el Despliegue

Una vez completado:
1. Obtendrás una URL como: `viajes-ai-abc123.vercel.app`
2. Visita la URL para verificar que funciona
3. Prueba hacer una pregunta de viaje

## 🔧 Estructura del Proyecto en Vercel

```
ViajeIA/
├── frontend/          # React app (se construye y despliega)
│   ├── build/        # Output de producción (generado por Vercel)
│   └── src/
├── api/              # Serverless functions (detectadas automáticamente)
│   ├── planificar.py
│   ├── health.py
│   └── requirements.txt
└── vercel.json       # Configuración de Vercel
```

## 📝 Notas Importantes

1. **Rutas API**: El frontend usa rutas relativas (`/api/planificar`) que funcionan automáticamente en Vercel
2. **Serverless Functions**: Las funciones en `api/` se convierten automáticamente en endpoints serverless
3. **Variables de Entorno**: Asegúrate de configurarlas en Vercel Dashboard
4. **Build Automático**: Cada push a `main` desplegará automáticamente

## 🐛 Solución de Problemas

### Error: "Module not found"
- Verifica que `api/requirements.txt` tenga todas las dependencias
- Verifica que `frontend/package.json` esté correcto

### Error: "API route not found"
- Verifica que los archivos en `api/` tengan la estructura correcta
- Verifica que `vercel.json` tenga las rutas configuradas

### Error: "Environment variable not found"
- Verifica que todas las variables estén en Vercel Dashboard
- Asegúrate de que estén marcadas para el entorno correcto

## ✅ Checklist Final

- [x] vercel.json configurado
- [x] Frontend actualizado para usar rutas relativas
- [ ] Cambios subidos a GitHub
- [ ] Proyecto conectado en Vercel
- [ ] Variables de entorno configuradas
- [ ] Primer despliegue completado
- [ ] Aplicación funcionando en producción

¡Listo! Tu aplicación estará en línea en minutos. 🎉

