# 🚀 Guía de Despliegue en Vercel - ViajeIA

Esta guía te ayudará a desplegar tu aplicación ViajeIA en Vercel de forma **completamente gratuita**.

## ⚡ Resumen Rápido

1. ✅ **Archivos ya creados:** `vercel.json`, `backend/api/planificar.py`, `backend/api/health.py`
2. 📤 Sube tu proyecto a GitHub
3. 🔗 Conecta Vercel con GitHub
4. ⚙️ Configura variables de entorno en Vercel
5. 🚀 ¡Despliega!

**Tiempo estimado:** 15-20 minutos

---

## 📋 Requisitos Previos

1. **Cuenta de GitHub** (gratuita) - [Crear cuenta](https://github.com/signup)
2. **Cuenta de Vercel** (gratuita) - [Crear cuenta](https://vercel.com/signup)
3. **Git instalado** en tu computadora

---

## 🎯 Paso 1: Preparar el Proyecto para Git

### 1.1 Inicializar Git (si no lo has hecho)

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
cd "C:\Users\mauri\Desktop\APPS AI\ViajeIA"
git init
```

### 1.2 Crear archivo .gitignore (si no existe)

Asegúrate de que `.gitignore` incluya:

```
# Dependencias
node_modules/
venv/
__pycache__/
*.pyc

# Variables de entorno
.env
.env.local
.env.development
.env.production

# Build
frontend/build/
dist/

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

### 1.3 Hacer commit inicial

```powershell
git add .
git commit -m "Initial commit - ViajeIA ready for deployment"
```

---

## 🎯 Paso 2: Subir a GitHub

### 2.1 Crear repositorio en GitHub

1. Ve a [github.com](https://github.com) e inicia sesión
2. Haz clic en el botón **"+"** (arriba derecha) → **"New repository"**
3. Nombre del repositorio: `viajeia` (o el que prefieras)
4. **NO marques** "Initialize with README"
5. Haz clic en **"Create repository"**

### 2.2 Conectar tu proyecto local con GitHub

GitHub te mostrará comandos. Ejecuta estos en PowerShell:

```powershell
# Reemplaza TU_USUARIO con tu usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/viajeia.git
git branch -M main
git push -u origin main
```

**Nota:** Si te pide autenticación, GitHub ahora usa tokens personales. Ve a:
- GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Genera un nuevo token con permisos `repo`
- Úsalo como contraseña cuando Git te lo pida

---

## 🎯 Paso 3: Configurar Vercel para el Frontend

### 3.1 Conectar Vercel con GitHub

1. Ve a [vercel.com](https://vercel.com) e inicia sesión
2. Haz clic en **"Add New..."** → **"Project"**
3. Selecciona **"Import Git Repository"**
4. Conecta tu cuenta de GitHub si es la primera vez
5. Selecciona el repositorio `viajeia`

### 3.2 Configurar el proyecto Frontend

En la configuración del proyecto:

- **Framework Preset:** React
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `build`
- **Install Command:** `npm install`

### 3.3 Variables de Entorno del Frontend

**IMPORTANTE:** No agregues `REACT_APP_API_URL` todavía. Primero necesitamos desplegar para obtener la URL. Lo haremos después del primer despliegue.

### 3.4 Desplegar Frontend

Haz clic en **"Deploy"**. Vercel construirá y desplegará tu frontend automáticamente.

---

## 🎯 Paso 4: Archivos ya Creados

¡Buenas noticias! Ya he creado los archivos necesarios para Vercel:

✅ **`vercel.json`** - Configuración de Vercel
✅ **`backend/api/planificar.py`** - Endpoint principal adaptado
✅ **`backend/api/health.py`** - Endpoint de salud

### 4.1 Verificar estructura

Tu proyecto ahora tiene esta estructura:

```
ViajeIA/
  ├── vercel.json          ✅ (ya creado)
  ├── backend/
  │   ├── api/
  │   │   ├── planificar.py ✅ (ya creado)
  │   │   └── health.py     ✅ (ya creado)
  │   ├── app.py           (para desarrollo local)
  │   └── requirements.txt
  └── frontend/
      └── ...
```

### 4.2 Verificar `requirements.txt`

Asegúrate de que `backend/requirements.txt` incluya:

```
google-generativeai
requests
```

**Nota:** Flask y flask-cors NO son necesarios para Vercel (solo para desarrollo local).

Este será el endpoint principal adaptado para Vercel:

```python
from vercel import Response
import os
import json
import re
import requests
from datetime import datetime
import google.generativeai as genai

# Configurar Gemini
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)

# Almacenamiento en memoria (para producción, usa Redis o similar)
conversation_history = {}
session_destinations = {}

# Importar funciones auxiliares desde un módulo compartido
# Por ahora, las incluimos aquí para simplificar

def obtener_clima_ciudad(ciudad):
    """Obtiene el clima actual de una ciudad usando Weatherbit API"""
    WEATHERBIT_API_KEY = os.environ.get('WEATHERBIT_API_KEY')
    if not WEATHERBIT_API_KEY:
        return None
    
    try:
        url = f"https://api.weatherbit.io/v2.0/current"
        params = {
            'city': ciudad,
            'key': WEATHERBIT_API_KEY,
            'lang': 'es'
        }
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                weather = data['data'][0]
                return {
                    'ciudad': weather.get('city_name', ciudad),
                    'temperatura': weather.get('temp', 'N/A'),
                    'descripcion': weather.get('weather', {}).get('description', 'N/A'),
                    'sensacion_termica': weather.get('app_temp', 'N/A'),
                    'humedad': weather.get('rh', 'N/A'),
                    'viento': weather.get('wind_spd', 'N/A')
                }
    except Exception as e:
        print(f"Error obteniendo clima: {str(e)}")
    
    return None

def obtener_fotos_unsplash(destino, cantidad=3):
    """Obtiene fotos de un destino usando Unsplash API"""
    api_key = os.environ.get('UNSPLASH_ACCESS_KEY') or os.environ.get('UNSPLASH_API_KEY')
    if not api_key:
        return []
    
    try:
        url = "https://api.unsplash.com/search/photos"
        headers = {'Authorization': f'Client-ID {api_key}'}
        params = {
            'query': destino,
            'per_page': cantidad,
            'orientation': 'landscape',
            'order_by': 'popularity'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                fotos = []
                for foto in data['results'][:cantidad]:
                    fotos.append({
                        'url': foto['urls']['regular'],
                        'url_small': foto['urls']['small'],
                        'url_thumb': foto['urls']['thumb'],
                        'autor': foto['user']['name'],
                        'autor_url': foto['user']['links']['html'],
                        'descripcion': foto.get('description', '') or foto.get('alt_description', '') or f'Foto de {destino}'
                    })
                return fotos
    except Exception as e:
        print(f"Error obteniendo fotos: {str(e)}")
    
    return []

def extraer_destinos(pregunta):
    """Intenta extraer nombres de ciudades/destinos de la pregunta"""
    ciudades_comunes = [
        'paris', 'parís', 'london', 'londres', 'tokyo', 'tokio', 'new york', 
        'nueva york', 'mexico', 'méxico', 'barcelona', 'madrid', 'roma', 'rome',
        'bogota', 'bogotá', 'buenos aires', 'lima', 'santiago', 'rio de janeiro',
        'cancun', 'cancún', 'playa del carmen', 'tulum', 'bali', 'bangkok',
        'dubai', 'singapore', 'singapur', 'sydney', 'sídney', 'melbourne'
    ]
    
    pregunta_lower = pregunta.lower()
    destinos_encontrados = []
    
    for ciudad in ciudades_comunes:
        if ciudad in pregunta_lower:
            destinos_encontrados.append(ciudad.title())
    
    if not destinos_encontrados:
        patrones = [
            r'planear\s+un\s+viaje\s+a\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
            r'viaje\s+a\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
            r'(?:a|en|desde|hacia|hasta)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
        ]
        
        for patron in patrones:
            matches = re.findall(patron, pregunta)
            if matches:
                for match in matches:
                    destino = match.strip()
                    destino = re.sub(r'\s+(desde|hasta|hacia|con|y|o|mi|el|la|los|las).*$', '', destino, flags=re.IGNORECASE)
                    if destino and len(destino) > 2:
                        destinos_encontrados.append(destino)
                        break
                if destinos_encontrados:
                    break
    
    return destinos_encontrados[:1] if destinos_encontrados else []

def handler(request):
    """Handler principal para Vercel"""
    if request.method != 'POST':
        return Response({'error': 'Método no permitido'}, status=405)
    
    try:
        data = request.json if hasattr(request, 'json') else json.loads(request.body)
        pregunta = data.get('pregunta', '')
        session_id = data.get('session_id', request.headers.get('x-forwarded-for', 'unknown'))
        
        if not pregunta:
            return Response({'error': 'No se proporcionó pregunta'}, status=400)
        
        # Obtener historial
        historial = conversation_history.get(session_id, [])
        es_primera_pregunta = len(historial) == 0
        
        # Extraer destinos
        destinos = extraer_destinos(pregunta)
        clima_data = None
        fotos_data = []
        destino_detectado = None
        
        if destinos and es_primera_pregunta:
            destino_principal = destinos[0]
            destino_detectado = destino_principal
            
            if os.environ.get('WEATHERBIT_API_KEY'):
                clima_data = obtener_clima_ciudad(destino_principal)
            
            if os.environ.get('UNSPLASH_ACCESS_KEY') or os.environ.get('UNSPLASH_API_KEY'):
                fotos_data = obtener_fotos_unsplash(destino_principal, cantidad=3)
        
        # Construir prompt
        if es_primera_pregunta:
            info_clima = ""
            if clima_data:
                info_clima = f"""
INFORMACIÓN DEL CLIMA ACTUAL:
🌡️ **Temperatura actual en {clima_data['ciudad']}**: {clima_data['temperatura']}°C
🌤️ **Condiciones**: {clima_data['descripcion']}
"""
            
            prompt = f"""Eres Axl, un consultor personal de viajes entusiasta y amigable.

⚠️⚠️⚠️ ESTRUCTURA OBLIGATORIA - DEBES SEGUIRLA EXACTAMENTE ⚠️⚠️⚠️

TU RESPUESTA DEBE COMENZAR INMEDIATAMENTE CON ESTA ESTRUCTURA EXACTA:

ALOJAMIENTO:
[recomendaciones detalladas con bullets (•)]

COMIDA LOCAL:
[recomendaciones con bullets (•)]

LUGARES IMPERDIBLES:
[lista con bullets (•)]

CONSEJOS LOCALES:
[tips especiales con bullets (•){info_clima}]

ESTIMACIÓN DE COSTOS:
[breakdown aproximado con bullets (•)]

REGLAS ESTRICTAS:
1. Comienza directamente con "ALOJAMIENTO:" sin introducción
2. Usa EXACTAMENTE estos títulos en mayúsculas seguidos de dos puntos
3. Cada título en su propia línea
4. Contenido con bullets (•) después de cada título
5. NO respondas en un solo párrafo
6. NO omitas ninguna sección

Pregunta del usuario: {pregunta}

Responde EXACTAMENTE con las 5 secciones en el orden especificado."""
        else:
            contexto_historial = ""
            if historial:
                contexto_historial = "\n\nCONTEXTO:\n"
                for preg, resp in historial[-3:]:
                    contexto_historial += f"P: {preg}\nR: {resp[:200]}...\n"
            
            prompt = f"""Eres Axl, un consultor personal de viajes.{contexto_historial}

El usuario hace una pregunta de seguimiento. Responde en MÁXIMO UN PÁRRAFO, de forma conversacional y concisa.

Pregunta: {pregunta}"""
        
        # Generar respuesta con Gemini
        if not GEMINI_API_KEY:
            return Response({'error': 'GEMINI_API_KEY no configurada'}, status=500)
        
        response = model.generate_content(prompt)
        respuesta = response.text
        
        # Guardar en historial
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        conversation_history[session_id].append((pregunta, respuesta))
        
        if len(conversation_history[session_id]) > 10:
            conversation_history[session_id] = conversation_history[session_id][-10:]
        
        if destino_detectado and es_primera_pregunta:
            session_destinations[session_id] = destino_detectado
        
        return Response({
            'respuesta': respuesta,
            'clima': clima_data,
            'fotos': fotos_data,
            'destino': destino_detectado,
            'session_id': session_id,
            'es_primera_pregunta': es_primera_pregunta,
            'historial': [{'pregunta': p, 'respuesta': r[:100] + '...' if len(r) > 100 else r} for p, r in historial]
        }, status=200)
    
    except Exception as e:
        return Response({'error': f'Error al procesar: {str(e)}'}, status=500)
```

### 4.4 Crear `backend/api/health.py`

```python
from vercel import Response

def handler(request):
    return Response({'status': 'ok', 'service': 'ViajeIA API'}, status=200)
```

### 4.5 Actualizar `requirements.txt`

Asegúrate de que `backend/requirements.txt` incluya:

```
google-generativeai
requests
python-dotenv
```

---

## 🎯 Paso 5: Variables de Entorno en Vercel

En el proyecto de Vercel, ve a **Settings** → **Environment Variables** y agrega:

```
GEMINI_API_KEY=AIzaSyBgtKCWZ7IbPujHbfCuCihRfXW3B3VMsb4
GEMINI_MODEL=gemini-2.0-flash
WEATHERBIT_API_KEY=dbc51eb5faf3451da9f8855daf663c06
UNSPLASH_ACCESS_KEY=tu_unsplash_key_aqui
```

**Importante:** Marca estas variables para **Production**, **Preview** y **Development**.

---

## 🎯 Paso 6: Actualizar Frontend para Producción

### 6.1 Actualizar Frontend después del primer despliegue

**IMPORTANTE:** Después de que Vercel despliegue tu proyecto por primera vez, obtendrás una URL como `viajeia-abc123.vercel.app`.

1. Ve a **Settings** → **Environment Variables** en Vercel
2. Agrega:
   ```
   REACT_APP_API_URL=https://TU_PROYECTO.vercel.app
   ```
   (Reemplaza `TU_PROYECTO` con tu URL real de Vercel)
3. Haz un nuevo despliegue (Vercel lo hará automáticamente cuando hagas push)

### 6.2 CORS

El backend de Vercel maneja CORS automáticamente. No necesitas configuración adicional.

---

## 🎯 Paso 7: Desplegar

### 7.1 Hacer commit y push

```powershell
git add .
git commit -m "Configure for Vercel deployment"
git push origin main
```

### 7.2 Vercel desplegará automáticamente

Vercel detectará el push y desplegará automáticamente. Puedes ver el progreso en el dashboard de Vercel.

---

## 🎯 Paso 8: Verificar el Despliegue

1. Ve a tu proyecto en Vercel
2. Haz clic en el dominio proporcionado (ej: `viajeia.vercel.app`)
3. Prueba la aplicación

---

## 🔧 Solución de Problemas

### Error: "Module not found"
- Verifica que `requirements.txt` tenga todas las dependencias
- Asegúrate de que las rutas en `vercel.json` sean correctas

### Error: "Environment variable not found"
- Verifica que todas las variables estén en Vercel
- Asegúrate de que estén marcadas para el entorno correcto

### CORS Errors
- Vercel maneja CORS automáticamente para funciones serverless
- Verifica que `REACT_APP_API_URL` apunte a tu dominio de Vercel

### Backend no responde
- Verifica los logs en Vercel Dashboard → Functions
- Asegúrate de que la estructura de carpetas sea correcta

---

## 📝 Notas Importantes

1. **Límites de Vercel Gratuito:**
   - 100GB bandwidth/mes
   - Funciones serverless: 100GB-hours/mes
   - Suficiente para uso personal y proyectos pequeños

2. **Almacenamiento en Memoria:**
   - El historial de conversaciones se pierde al reiniciar
   - Para producción real, considera usar Redis o una base de datos

3. **Dominio Personalizado:**
   - Vercel permite agregar tu propio dominio gratis
   - Ve a Settings → Domains

---

## ✅ Checklist Final

- [ ] Proyecto subido a GitHub
- [ ] Vercel conectado con GitHub
- [ ] Variables de entorno configuradas
- [ ] `vercel.json` creado
- [ ] Estructura de API creada (`backend/api/`)
- [ ] Frontend desplegado
- [ ] Backend desplegado
- [ ] Aplicación funcionando en producción

---

¡Listo! Tu aplicación ViajeIA estará disponible en internet de forma gratuita. 🎉

