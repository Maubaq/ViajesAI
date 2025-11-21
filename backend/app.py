from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import google.generativeai as genai
import os
import re
import requests
from pathlib import Path

# Cargar variables de entorno de forma segura
try:
    from dotenv import load_dotenv
    # Cargar desde el directorio del backend
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()  # Intentar cargar desde el directorio actual
except Exception as e:
    print(f"Advertencia: No se pudo cargar dotenv: {e}")
    print("Continuando con variables de entorno del sistema...")

app = Flask(__name__)

# Configuración de CORS - Seguro para producción
allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, origins=allowed_origins, supports_credentials=True)

# Configurar la API Key de Gemini desde variables de entorno
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY no está configurada. Por favor, configura la variable de entorno.")

genai.configure(api_key=GEMINI_API_KEY)

# Configurar el modelo - Gemini 2.0 Flash
# Puedes cambiar el modelo desde la variable de entorno GEMINI_MODEL
# Opciones: 'gemini-2.0-flash', 'gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-pro'
# Nota: 'gemini-2.0-flash' es el modelo recomendado y funcional
model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
model = genai.GenerativeModel(model_name)

# Configurar API Key de Weatherbit (opcional)
WEATHERBIT_API_KEY = os.getenv('WEATHERBIT_API_KEY', '')

# Configurar API Key de Unsplash (opcional)
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY', '')
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY', '')  # Para acceso público

# Rate limiting simple (en producción usar Redis o similar)
request_counts = {}

# Historial de conversaciones por sesión (en producción usar Redis o base de datos)
conversation_history = {}
# Almacenar destino principal por sesión para mantener contexto
session_destinations = {}

def rate_limit(max_requests=10, window=60):
    """Decorador simple para rate limiting"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = __import__('time').time()
            
            # Limpiar entradas antiguas
            if client_ip in request_counts:
                request_counts[client_ip] = [
                    t for t in request_counts[client_ip] 
                    if current_time - t < window
                ]
            else:
                request_counts[client_ip] = []
            
            # Verificar límite
            if len(request_counts[client_ip]) >= max_requests:
                return jsonify({
                    'error': 'Demasiadas solicitudes. Por favor, espera un momento.'
                }), 429
            
            # Registrar solicitud
            request_counts[client_ip].append(current_time)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_input(text, max_length=2000):
    """Validar y sanitizar entrada del usuario"""
    if not text or not isinstance(text, str):
        return False, "El texto no es válido"
    
    if len(text.strip()) == 0:
        return False, "El texto no puede estar vacío"
    
    if len(text) > max_length:
        return False, f"El texto es demasiado largo (máximo {max_length} caracteres)"
    
    # Sanitizar: remover caracteres peligrosos pero permitir texto normal
    sanitized = re.sub(r'[<>]', '', text)
    
    return True, sanitized

def obtener_clima_ciudad(ciudad):
    """
    Obtiene el clima actual de una ciudad usando Weatherbit API
    Retorna un diccionario con la información del clima o None si hay error
    """
    if not WEATHERBIT_API_KEY:
        return None
    
    try:
        # Weatherbit API - Current Weather
        url = "https://api.weatherbit.io/v2.0/current"
        params = {
            'city': ciudad,
            'key': WEATHERBIT_API_KEY,
            'lang': 'es',
            'units': 'M'  # Métrico (Celsius)
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                clima = data['data'][0]
                return {
                    'temperatura': clima.get('temp', 'N/A'),
                    'descripcion': clima.get('weather', {}).get('description', 'N/A'),
                    'sensacion_termica': clima.get('app_temp', 'N/A'),
                    'humedad': clima.get('rh', 'N/A'),
                    'viento': clima.get('wind_spd', 'N/A'),
                    'ciudad': clima.get('city_name', ciudad),
                    'pais': clima.get('country_code', ''),
                    'icono': clima.get('weather', {}).get('icon', '')
                }
        elif response.status_code == 429:
            app.logger.warning("Límite de rate de Weatherbit alcanzado")
        else:
            app.logger.warning(f"Weatherbit API error: {response.status_code}")
    
    except Exception as e:
        app.logger.error(f"Error obteniendo clima: {str(e)}")
    
    return None

def obtener_tipo_cambio(base_currency='USD', target_currency='EUR'):
    """
    Obtiene el tipo de cambio usando exchangerate-api.com (gratuito)
    Retorna el tipo de cambio o None si hay error
    """
    try:
        # API gratuita sin key requerida
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if 'rates' in data and target_currency in data['rates']:
                rate = data['rates'][target_currency]
                return {
                    'base': base_currency,
                    'target': target_currency,
                    'rate': round(rate, 4),
                    'fecha': data.get('date', '')
                }
    except Exception as e:
        app.logger.error(f"Error obteniendo tipo de cambio: {str(e)}")
    
    return None

def obtener_diferencia_horaria(ciudad):
    """
    Obtiene la diferencia horaria de una ciudad usando worldtimeapi.org (gratuito)
    Retorna información de zona horaria o None si hay error
    """
    try:
        # Mapeo de ciudades comunes a zonas horarias
        timezone_map = {
            'paris': 'Europe/Paris',
            'parís': 'Europe/Paris',
            'barcelona': 'Europe/Madrid',
            'madrid': 'Europe/Madrid',
            'london': 'Europe/London',
            'londres': 'Europe/London',
            'tokyo': 'Asia/Tokyo',
            'tokio': 'Asia/Tokyo',
            'new york': 'America/New_York',
            'nueva york': 'America/New_York',
            'mexico': 'America/Mexico_City',
            'méxico': 'America/Mexico_City',
            'bogota': 'America/Bogota',
            'bogotá': 'America/Bogota',
            'buenos aires': 'America/Argentina/Buenos_Aires',
            'lima': 'America/Lima',
            'santiago': 'America/Santiago',
            'rio de janeiro': 'America/Sao_Paulo',
            'cancun': 'America/Cancun',
            'cancún': 'America/Cancun',
            'bali': 'Asia/Makassar',
            'bangkok': 'Asia/Bangkok',
            'dubai': 'Asia/Dubai',
            'singapore': 'Asia/Singapore',
            'singapur': 'Asia/Singapore',
            'sydney': 'Australia/Sydney',
            'sídney': 'Australia/Sydney',
        }
        
        ciudad_lower = ciudad.lower()
        timezone = timezone_map.get(ciudad_lower)
        
        if not timezone:
            # Intentar buscar por nombre parcial
            for key, tz in timezone_map.items():
                if key in ciudad_lower or ciudad_lower in key:
                    timezone = tz
                    break
        
        if timezone:
            url = f"http://worldtimeapi.org/api/timezone/{timezone}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                # Calcular diferencia con UTC
                utc_offset = data.get('utc_offset', '')
                datetime_str = data.get('datetime', '')
                
                # Obtener hora actual formateada
                hora_actual = None
                if datetime_str:
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
                        hora_actual = dt.strftime('%H:%M:%S')
                    except:
                        pass
                
                return {
                    'timezone': timezone,
                    'utc_offset': utc_offset,
                    'datetime': datetime_str,
                    'hora_actual': hora_actual,
                    'ciudad': ciudad
                }
    except Exception as e:
        app.logger.error(f"Error obteniendo diferencia horaria: {str(e)}")
    
    return None

def obtener_fotos_unsplash(destino, cantidad=3):
    """
    Obtiene fotos de un destino usando Unsplash API
    Retorna una lista de URLs de fotos o lista vacía si hay error
    """
    # Usar Access Key si está disponible, sino usar API Key
    api_key = UNSPLASH_ACCESS_KEY or UNSPLASH_API_KEY
    
    if not api_key:
        return []
    
    try:
        # Unsplash API - Search Photos
        url = "https://api.unsplash.com/search/photos"
        headers = {
            'Authorization': f'Client-ID {api_key}'
        }
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
                app.logger.info(f"Unsplash: {len(fotos)} fotos obtenidas para '{destino}'")
                return fotos
            else:
                app.logger.warning(f"Unsplash: No se encontraron resultados para '{destino}'")
        elif response.status_code == 401:
            app.logger.error(f"Unsplash API error 401: API Key inválida o no autorizada")
        elif response.status_code == 403:
            app.logger.error(f"Unsplash API error 403: Acceso denegado - verifica tu API key")
        else:
            app.logger.warning(f"Unsplash API error: {response.status_code} - {response.text[:200]}")
    
    except Exception as e:
        app.logger.error(f"Error obteniendo fotos de Unsplash: {str(e)}")
    
    return []

def extraer_destinos(pregunta):
    """
    Intenta extraer nombres de ciudades/destinos de la pregunta
    Retorna una lista de posibles destinos
    """
    # Lista de ciudades comunes para mejorar la detección
    ciudades_comunes = [
        'paris', 'parís', 'london', 'londres', 'tokyo', 'tokio', 'new york', 
        'nueva york', 'mexico', 'méxico', 'barcelona', 'madrid', 'roma', 'rome',
        'bogota', 'bogotá', 'buenos aires', 'lima', 'santiago', 'rio de janeiro',
        'cancun', 'cancún', 'playa del carmen', 'tulum', 'bali', 'bangkok',
        'dubai', 'singapore', 'singapur', 'sydney', 'sídney', 'melbourne'
    ]
    
    pregunta_lower = pregunta.lower()
    destinos_encontrados = []
    
    # Buscar ciudades comunes
    for ciudad in ciudades_comunes:
        if ciudad in pregunta_lower:
            destinos_encontrados.append(ciudad.title())
    
    # Si no encontramos ciudades conocidas, intentar extraer después de palabras clave
    if not destinos_encontrados:
        # Mejorar patrones para detectar destinos del formulario
        # Patrón específico para el formulario: "Quiero planear un viaje a [destino] desde..."
        patrones = [
            r'planear\s+un\s+viaje\s+a\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',  # "planear un viaje a Paris"
            r'viaje\s+a\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',  # "viaje a Paris"
            r'(?:a|en|desde|hacia|hasta)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',  # "a Paris"
            r'viajar\s+(?:a|a|en)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',  # "viajar a Paris"
            r'destino[:\s]+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',  # "destino: Paris"
            r'¿A\s+dónde\s+quieres\s+viajar\??\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',  # Para preguntas directas
        ]
        
        for patron in patrones:
            matches = re.findall(patron, pregunta)
            if matches:
                # Limpiar el destino encontrado (remover palabras comunes que no son parte del nombre)
                for match in matches:
                    destino = match.strip()
                    # Remover palabras comunes que pueden aparecer después del destino
                    destino = re.sub(r'\s+(desde|hasta|hacia|con|y|o|mi|el|la|los|las).*$', '', destino, flags=re.IGNORECASE)
                    if destino and len(destino) > 2:  # Asegurar que tiene al menos 3 caracteres
                        destinos_encontrados.append(destino)
                if destinos_encontrados:
                    break
    
    # Si aún no encontramos nada, intentar extraer cualquier palabra capitalizada después de "a"
    if not destinos_encontrados:
        # Buscar patrones más flexibles - incluir acentos y caracteres especiales
        match = re.search(r'\b(?:a|en|viaje\s+a|viajar\s+a|planear\s+un\s+viaje\s+a)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)', pregunta, re.IGNORECASE)
        if match:
            destino = match.group(1).strip()
            # Remover palabras comunes
            destino = re.sub(r'\s+(desde|hasta|hacia|con|y|o|mi|el|la|los|las).*$', '', destino, flags=re.IGNORECASE)
            if destino and len(destino) > 2:
                destinos_encontrados.append(destino)
    
    # Si aún no encontramos nada, intentar buscar cualquier palabra capitalizada que parezca un lugar
    # después de "viaje a" o "a" (último recurso)
    if not destinos_encontrados:
        # Buscar "viaje a [palabra capitalizada]" de forma más flexible
        match = re.search(r'(?:viaje|viajar|planear.*viaje).*?\ba\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[a-záéíóúñ]+)*)', pregunta, re.IGNORECASE)
        if match:
            destino = match.group(1).strip()
            # Remover palabras comunes al final
            destino = re.sub(r'\s+(desde|hasta|hacia|con|y|o|mi|el|la|los|las|un|una|unos|unas).*$', '', destino, flags=re.IGNORECASE)
            if destino and len(destino) > 2:
                destinos_encontrados.append(destino)
    
    # Log para debugging
    if destinos_encontrados:
        app.logger.info(f"Destinos detectados: {destinos_encontrados}")
    else:
        app.logger.warning(f"No se detectaron destinos en: {pregunta[:100]}")
    
    return destinos_encontrados

@app.route('/api/planificar', methods=['POST'])
@rate_limit(max_requests=10, window=60)
def planificar_viaje():
    try:
        # Validar Content-Type
        if not request.is_json:
            return jsonify({'error': 'Content-Type debe ser application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        pregunta = data.get('pregunta', '')
        session_id = data.get('session_id', request.remote_addr)
        
        # Validar y sanitizar entrada
        is_valid, result = validate_input(pregunta)
        if not is_valid:
            return jsonify({'error': result}), 400
        
        pregunta = result
        
        # Obtener historial de conversación si existe
        historial = conversation_history.get(session_id, [])
        es_primera_pregunta = len(historial) == 0
        
        app.logger.info(f"🔍 Sesión: {session_id}, Es primera pregunta: {es_primera_pregunta}, Historial: {len(historial)} preguntas")
        
        # Intentar extraer destinos y obtener clima y fotos (solo en primera pregunta o si se menciona nuevo destino)
        destinos = extraer_destinos(pregunta)
        clima_data = None
        fotos_data = []
        info_clima = ""
        destino_detectado = None
        
        # Solo buscar clima y fotos en primera pregunta
        if destinos and es_primera_pregunta:
            destino_principal = destinos[0]
            destino_detectado = destino_principal
            
            app.logger.info(f"🎯 Destino detectado: {destino_principal}")
            
            # Obtener clima si hay API key
            if WEATHERBIT_API_KEY:
                app.logger.info(f"🌤️ Buscando clima para: {destino_principal}")
                clima_data = obtener_clima_ciudad(destino_principal)
                if clima_data:
                    app.logger.info(f"✅ Clima obtenido exitosamente para {destino_principal}")
                    info_clima = f"""

INFORMACIÓN DEL CLIMA ACTUAL:
🌡️ **Temperatura actual en {clima_data['ciudad']}**: {clima_data['temperatura']}°C
🌤️ **Condiciones**: {clima_data['descripcion']}
🌡️ **Sensación térmica**: {clima_data['sensacion_termica']}°C
💧 **Humedad**: {clima_data['humedad']}%
💨 **Viento**: {clima_data['viento']} m/s

Usa esta información del clima para dar recomendaciones sobre qué ropa llevar y actividades apropiadas para las condiciones climáticas actuales."""
                else:
                    app.logger.warning(f"⚠️ No se pudo obtener clima para {destino_principal}")
            else:
                app.logger.warning("⚠️ Weatherbit API key no configurada")
            
            # Obtener fotos automáticamente si hay API key
            if UNSPLASH_ACCESS_KEY or UNSPLASH_API_KEY:
                app.logger.info(f"📸 Buscando fotos para: {destino_principal}")
                fotos_data = obtener_fotos_unsplash(destino_principal, cantidad=3)
                if fotos_data:
                    app.logger.info(f"✅ Fotos obtenidas exitosamente: {len(fotos_data)} fotos para {destino_principal}")
                else:
                    app.logger.warning(f"⚠️ No se pudieron obtener fotos para {destino_principal}")
            else:
                app.logger.warning("⚠️ Unsplash API key no configurada - las fotos no se obtendrán")
                app.logger.info("💡 Para habilitar fotos automáticas, agrega UNSPLASH_ACCESS_KEY a backend/.env")
                app.logger.info("💡 Ver instrucciones en UNSPLASH_SETUP.md")
        elif historial and not destinos:
            # En preguntas de seguimiento, usar el destino de la primera pregunta si está disponible
            if session_id in session_destinations:
                destino_detectado = session_destinations[session_id]
                app.logger.info(f"📍 Usando destino de sesión anterior: {destino_detectado}")
        
        # Obtener destino de la sesión si existe
        destino_sesion = session_destinations.get(session_id, None)
        
        # Construir contexto del historial
        contexto_historial = ""
        if historial:
            contexto_historial = "\n\nCONTEXTO DE LA CONVERSACIÓN ANTERIOR:\n"
            for i, (preg, resp) in enumerate(historial[-3:], 1):  # Últimas 3 interacciones
                contexto_historial += f"\nPregunta {i}: {preg}\nRespuesta {i}: {resp[:200]}...\n"
        
        # Agregar información del destino al contexto si existe
        if destino_sesion and not es_primera_pregunta:
            contexto_historial += f"\n\nIMPORTANTE: El usuario está preguntando sobre {destino_sesion}. Cuando use palabras como 'allí', 'ese lugar', 'ese destino', 'el transporte allí', etc., se refiere a {destino_sesion}."
        
        # Crear el prompt para Axl, el consultor personal de viajes
        if es_primera_pregunta:
            # Primera pregunta: estructura completa requerida
            app.logger.info("📝 Generando prompt para PRIMERA PREGUNTA - estructura completa obligatoria")
            prompt = f"""Eres Axl, un consultor personal de viajes entusiasta y amigable. Tu personalidad es:
            
- Te presentas siempre como "Axl, tu consultor personal de viajes" 🧳
- Eres muy entusiasta, amigable y positivo
- Das respuestas organizadas y estructuradas
- Usas emojis de viajes relevantes (✈️ 🧳 🗺️ 🏨 🍽️ 🎫 🌍 🏖️ 🏛️ 🎨 etc.)
- Formateas el texto usando **texto** para negritas (el usuario verá esto resaltado)

⚠️⚠️⚠️ ESTRUCTURA OBLIGATORIA - DEBES SEGUIRLA EXACTAMENTE ⚠️⚠️⚠️

TU RESPUESTA DEBE COMENZAR INMEDIATAMENTE CON ESTA ESTRUCTURA EXACTA. NO AGREGUES INTRODUCCIÓN NI SALUDO ANTES DE LAS SECCIONES.

FORMATO EXACTO OBLIGATORIO (copia y pega esta estructura, solo reemplaza el contenido entre corchetes):

ALOJAMIENTO:
[recomendaciones detalladas de hoteles, hostales, Airbnb, etc. con precios aproximados, ubicaciones y características. Usa bullets (•) para organizar.]

COMIDA LOCAL:
[recomendaciones de restaurantes, platos típicos, lugares para comer, precios aproximados, y experiencias gastronómicas. Usa bullets (•) para organizar.]

LUGARES IMPERDIBLES:
[lista de lugares que no se pueden perder, con descripciones breves, horarios y tips de visita. Usa bullets (•) para organizar.]

CONSEJOS LOCALES:
[tips especiales, advertencias, costumbres locales, qué evitar, transporte, seguridad, y cualquier información práctica importante. Usa bullets (•) para organizar.{info_clima}]

ESTIMACIÓN DE COSTOS:
[breakdown aproximado de costos diarios/semanales: alojamiento, comida, transporte, actividades, entretenimiento, etc. Usa bullets (•) para organizar.]

REGLAS ESTRICTAS - DEBES SEGUIRLAS SIN EXCEPCIÓN:
1. TU RESPUESTA DEBE COMENZAR DIRECTAMENTE CON "ALOJAMIENTO:" (sin introducción previa)
2. DEBES usar EXACTAMENTE estos títulos en este orden exacto:
   - ALOJAMIENTO:
   - COMIDA LOCAL:
   - LUGARES IMPERDIBLES:
   - CONSEJOS LOCALES:
   - ESTIMACIÓN DE COSTOS:
3. Cada título DEBE estar en MAYÚSCULAS, seguido de DOS PUNTOS (:), y en su propia línea
4. Después de cada título, DEBES incluir contenido detallado con bullets (•)
5. NO respondas en un solo párrafo
6. NO omitas ninguna sección
7. NO cambies el orden de las secciones
8. NO uses emojis en los títulos (solo el texto exacto: ALOJAMIENTO:, COMIDA LOCAL:, etc.)
9. NO agregues texto antes de "ALOJAMIENTO:"
10. Todas las 5 secciones son OBLIGATORIAS

EJEMPLO DE FORMATO CORRECTO (tu respuesta debe verse así):
ALOJAMIENTO:
• Hotel XYZ - $100/noche - Ubicado en el centro
• Hostal ABC - $30/noche - Ambiente joven y social

COMIDA LOCAL:
• Restaurante DEF - Platos típicos desde $15
• Mercado local - Comida callejera desde $5

LUGARES IMPERDIBLES:
• Plaza Principal - Visita recomendada en la mañana
• Museo de Arte - Abierto de 9am a 6pm

CONSEJOS LOCALES:
• Lleva efectivo para mercados locales
• Evita taxis no oficiales

ESTIMACIÓN DE COSTOS:
• Alojamiento: $50-100/día
• Comida: $20-40/día
• Transporte: $10-20/día

Pregunta del usuario: {pregunta}

IMPORTANTE: Esta es la PRIMERA PREGUNTA. Tu respuesta DEBE comenzar directamente con "ALOJAMIENTO:" sin introducción. Responde EXACTAMENTE con las 5 secciones en el orden especificado. NO uses un solo párrafo. NO omitas ninguna sección."""
        else:
            # Preguntas de seguimiento: respuesta libre y concisa (máximo un párrafo)
            app.logger.info("📝 Generando prompt para PREGUNTA DE SEGUIMIENTO - respuesta concisa en un párrafo")
            prompt = f"""Eres Axl, un consultor personal de viajes entusiasta y amigable.{contexto_historial}

El usuario está haciendo una pregunta de seguimiento sobre el mismo destino. Responde de manera conversacional, útil y CONCISA.

⚠️⚠️⚠️ ESTA ES UNA PREGUNTA DE SEGUIMIENTO - RESPUESTA CONCISA ⚠️⚠️⚠️

INSTRUCCIONES ESTRICTAS PARA PREGUNTAS DE SEGUIMIENTO:
- Responde en MÁXIMO UN PÁRRAFO (no más de 4-5 oraciones)
- Sé directo, específico y útil
- Responde de forma natural y conversacional, como si estuvieras teniendo una charla
- Usa **texto entre dos asteriscos** para resaltar información importante si es necesario
- Incluye 1-2 emojis relevantes si aportan valor
- NO uses bullets (•) ni listas - solo texto fluido en párrafo
- NO uses estructura de secciones (no uses 🏨 🍽️ 📍 💡 💰)
- NO repitas información que ya diste antes - sé conciso
- Si la pregunta requiere información que ya diste, haz una referencia breve a la respuesta anterior
- Mantén el tono entusiasta y amigable pero sé breve

IMPORTANTE: Tu respuesta DEBE ser UN SOLO PÁRRAFO. No uses estructura de secciones, no uses bullets, solo texto fluido y natural en un párrafo continuo.

Pregunta actual del usuario: {pregunta}

Responde como Axl, siendo entusiasta, amigable, útil y CONCISO (máximo un párrafo, sin secciones)."""
        
        # Generar respuesta con Gemini
        response = model.generate_content(prompt)
        respuesta = response.text
        
        # Guardar destino en la sesión si es la primera pregunta y hay destino
        if destino_detectado and es_primera_pregunta:
            session_destinations[session_id] = destino_detectado
            app.logger.info(f"💾 Destino guardado para sesión {session_id}: {destino_detectado}")
        
        # Guardar en historial de conversación
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        conversation_history[session_id].append((pregunta, respuesta))
        
        # Limitar historial a 10 interacciones por sesión
        if len(conversation_history[session_id]) > 10:
            conversation_history[session_id] = conversation_history[session_id][-10:]
        
        # Obtener información adicional para el panel lateral (solo si hay destino)
        info_adicional = {}
        destino_para_info = destino_detectado or destino_sesion or (destinos[0] if destinos else None)
        
        if destino_para_info:
            app.logger.info(f"Obteniendo información adicional para: {destino_para_info}")
            
            # Obtener tipo de cambio (USD a EUR como ejemplo)
            tipo_cambio = obtener_tipo_cambio('USD', 'EUR')
            if tipo_cambio:
                info_adicional['tipo_cambio'] = tipo_cambio
                app.logger.info(f"Tipo de cambio obtenido: {tipo_cambio}")
            else:
                app.logger.warning("No se pudo obtener tipo de cambio")
            
            # Obtener diferencia horaria
            diferencia_horaria = obtener_diferencia_horaria(destino_para_info)
            if diferencia_horaria:
                info_adicional['diferencia_horaria'] = diferencia_horaria
                app.logger.info(f"Diferencia horaria obtenida: {diferencia_horaria}")
            else:
                app.logger.warning(f"No se pudo obtener diferencia horaria para {destino_para_info}")
        else:
            app.logger.warning("No hay destino detectado para obtener información adicional")
        
        # Preparar respuesta con clima y fotos
        destino_final = destino_detectado or destino_sesion or (destinos[0] if destinos else None)
        respuesta_json = {
            'respuesta': respuesta,
            'clima': clima_data,
            'fotos': fotos_data,
            'destino': destino_final,
            'session_id': session_id,
            'es_primera_pregunta': es_primera_pregunta,
            'info_adicional': info_adicional if info_adicional else None,
            'historial': [{'pregunta': p, 'respuesta': r[:100] + '...' if len(r) > 100 else r} for p, r in historial] if historial else []
        }
        
        # Log para debugging
        app.logger.info(f"📤 Respuesta preparada:")
        app.logger.info(f"   - Es primera pregunta: {es_primera_pregunta}")
        app.logger.info(f"   - Clima: {clima_data is not None} ({clima_data['ciudad'] if clima_data else 'N/A'})")
        app.logger.info(f"   - Fotos: {len(fotos_data)} fotos")
        app.logger.info(f"   - Destino: {respuesta_json['destino']}")
        app.logger.info(f"   - Info adicional: {bool(info_adicional)}")
        app.logger.info(f"   - Longitud respuesta: {len(respuesta)} caracteres")
        
        return jsonify(respuesta_json), 200
    
    except Exception as e:
        error_message = str(e)
        # Log detallado para debugging (solo en desarrollo)
        app.logger.error(f"Error en planificar_viaje: {error_message}")
        
        # Manejar errores específicos de la API
        if 'API_KEY' in error_message or 'quota' in error_message.lower() or 'permission' in error_message.lower():
            return jsonify({
                'error': 'Error con la API de Gemini. Por favor, verifica la configuración.',
                'details': error_message if os.getenv('FLASK_DEBUG', 'False').lower() == 'true' else None
            }), 500
        elif 'model' in error_message.lower() or 'not found' in error_message.lower():
            return jsonify({
                'error': f'Error con el modelo de Gemini. Verifica que el modelo esté disponible. Error: {error_message}',
                'details': error_message if os.getenv('FLASK_DEBUG', 'False').lower() == 'true' else None
            }), 500
        return jsonify({
            'error': 'Error al procesar la solicitud. Por favor, intenta de nuevo.',
            'details': error_message if os.getenv('FLASK_DEBUG', 'False').lower() == 'true' else None
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'service': 'ViajeIA API'}), 200

# Headers de seguridad
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

if __name__ == '__main__':
    # En desarrollo
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

