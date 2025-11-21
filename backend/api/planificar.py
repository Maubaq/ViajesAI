from http.server import BaseHTTPRequestHandler
import json
import os
import re
import requests
import google.generativeai as genai

# Configurar Gemini
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)

# Almacenamiento en memoria (para producción, usa Redis)
conversation_history = {}
session_destinations = {}

def obtener_clima_ciudad(ciudad):
    """Obtiene el clima actual de una ciudad usando Weatherbit API"""
    WEATHERBIT_API_KEY = os.environ.get('WEATHERBIT_API_KEY')
    if not WEATHERBIT_API_KEY:
        return None
    
    try:
        url = "https://api.weatherbit.io/v2.0/current"
        params = {
            'city': ciudad,
            'key': WEATHERBIT_API_KEY,
            'lang': 'es',
            'units': 'M'
        }
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
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

def obtener_tipo_cambio(base_currency='USD', target_currency='EUR'):
    """Obtiene el tipo de cambio usando exchangerate-api.com"""
    try:
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
        print(f"Error obteniendo tipo de cambio: {str(e)}")
    
    return None

def obtener_diferencia_horaria(ciudad):
    """Obtiene la diferencia horaria usando worldtimeapi.org"""
    try:
        timezone_map = {
            'paris': 'Europe/Paris', 'parís': 'Europe/Paris',
            'barcelona': 'Europe/Madrid', 'madrid': 'Europe/Madrid',
            'london': 'Europe/London', 'londres': 'Europe/London',
            'tokyo': 'Asia/Tokyo', 'tokio': 'Asia/Tokyo',
            'new york': 'America/New_York', 'nueva york': 'America/New_York',
            'mexico': 'America/Mexico_City', 'méxico': 'America/Mexico_City',
            'bogota': 'America/Bogota', 'bogotá': 'America/Bogota',
            'buenos aires': 'America/Argentina/Buenos_Aires',
            'lima': 'America/Lima', 'santiago': 'America/Santiago',
            'rio de janeiro': 'America/Sao_Paulo',
            'cancun': 'America/Cancun', 'cancún': 'America/Cancun',
            'bali': 'Asia/Makassar', 'bangkok': 'Asia/Bangkok',
            'dubai': 'Asia/Dubai', 'singapore': 'Asia/Singapore',
            'singapur': 'Asia/Singapore', 'sydney': 'Australia/Sydney',
            'sídney': 'Australia/Sydney',
        }
        
        ciudad_lower = ciudad.lower()
        timezone = timezone_map.get(ciudad_lower)
        
        if not timezone:
            for key, tz in timezone_map.items():
                if key in ciudad_lower or ciudad_lower in key:
                    timezone = tz
                    break
        
        if timezone:
            url = f"http://worldtimeapi.org/api/timezone/{timezone}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'timezone': timezone,
                    'utc_offset': data.get('utc_offset', ''),
                    'datetime': data.get('datetime', ''),
                    'ciudad': ciudad
                }
    except Exception as e:
        print(f"Error obteniendo diferencia horaria: {str(e)}")
    
    return None

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

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            pregunta = data.get('pregunta', '')
            session_id = data.get('session_id', self.headers.get('x-forwarded-for', 'unknown'))
            
            if not pregunta:
                self.send_error_response(400, 'No se proporcionó pregunta')
                return
            
            # Obtener historial
            historial = conversation_history.get(session_id, [])
            es_primera_pregunta = len(historial) == 0
            
            # Extraer destinos
            destinos = extraer_destinos(pregunta)
            clima_data = None
            fotos_data = []
            destino_detectado = None
            info_clima = ""
            
            if destinos and es_primera_pregunta:
                destino_principal = destinos[0]
                destino_detectado = destino_principal
                
                if os.environ.get('WEATHERBIT_API_KEY'):
                    clima_data = obtener_clima_ciudad(destino_principal)
                    if clima_data:
                        info_clima = f"""

INFORMACIÓN DEL CLIMA ACTUAL:
🌡️ **Temperatura actual en {clima_data['ciudad']}**: {clima_data['temperatura']}°C
🌤️ **Condiciones**: {clima_data['descripcion']}
🌡️ **Sensación térmica**: {clima_data['sensacion_termica']}°C
💧 **Humedad**: {clima_data['humedad']}%
💨 **Viento**: {clima_data['viento']} m/s

Usa esta información del clima para dar recomendaciones sobre qué ropa llevar y actividades apropiadas para las condiciones climáticas actuales."""
                
                if os.environ.get('UNSPLASH_ACCESS_KEY') or os.environ.get('UNSPLASH_API_KEY'):
                    fotos_data = obtener_fotos_unsplash(destino_principal, cantidad=3)
            elif historial and not destinos:
                if session_id in session_destinations:
                    destino_detectado = session_destinations[session_id]
            
            destino_sesion = session_destinations.get(session_id, None)
            
            # Construir contexto del historial
            contexto_historial = ""
            if historial:
                contexto_historial = "\n\nCONTEXTO DE LA CONVERSACIÓN ANTERIOR:\n"
                for i, (preg, resp) in enumerate(historial[-3:], 1):
                    contexto_historial += f"\nPregunta {i}: {preg}\nRespuesta {i}: {resp[:200]}...\n"
            
            if destino_sesion and not es_primera_pregunta:
                contexto_historial += f"\n\nIMPORTANTE: El usuario está preguntando sobre {destino_sesion}. Cuando use palabras como 'allí', 'ese lugar', 'ese destino', 'el transporte allí', etc., se refiere a {destino_sesion}."
            
            # Crear prompt
            if es_primera_pregunta:
                prompt = f"""Eres Axl, un consultor personal de viajes entusiasta y amigable.

⚠️⚠️⚠️ ESTRUCTURA OBLIGATORIA - DEBES SEGUIRLA EXACTAMENTE ⚠️⚠️⚠️

TU RESPUESTA DEBE COMENZAR INMEDIATAMENTE CON ESTA ESTRUCTURA EXACTA. NO AGREGUES INTRODUCCIÓN NI SALUDO ANTES DE LAS SECCIONES.

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
8. NO uses emojis en los títulos (solo el texto exacto)
9. NO agregues texto antes de "ALOJAMIENTO:"
10. Todas las 5 secciones son OBLIGATORIAS

Pregunta del usuario: {pregunta}

IMPORTANTE: Esta es la PRIMERA PREGUNTA. Tu respuesta DEBE comenzar directamente con "ALOJAMIENTO:" sin introducción. Responde EXACTAMENTE con las 5 secciones en el orden especificado."""
            else:
                prompt = f"""Eres Axl, un consultor personal de viajes entusiasta y amigable.{contexto_historial}

El usuario está haciendo una pregunta de seguimiento sobre el mismo destino. Responde de manera conversacional, útil y CONCISA.

⚠️⚠️⚠️ ESTA ES UNA PREGUNTA DE SEGUIMIENTO - RESPUESTA CONCISA ⚠️⚠️⚠️

INSTRUCCIONES ESTRICTAS PARA PREGUNTAS DE SEGUIMIENTO:
- Responde en MÁXIMO UN PÁRRAFO (no más de 4-5 oraciones)
- Sé directo, específico y útil
- Responde de forma natural y conversacional
- Usa **texto entre dos asteriscos** para resaltar información importante si es necesario
- Incluye 1-2 emojis relevantes si aportan valor
- NO uses bullets (•) ni listas - solo texto fluido en párrafo
- NO uses estructura de secciones
- NO repitas información que ya diste antes - sé conciso

IMPORTANTE: Tu respuesta DEBE ser UN SOLO PÁRRAFO. No uses estructura de secciones, no uses bullets, solo texto fluido y natural.

Pregunta actual del usuario: {pregunta}

Responde como Axl, siendo entusiasta, amigable, útil y CONCISO (máximo un párrafo, sin secciones)."""
            
            # Generar respuesta con Gemini
            if not GEMINI_API_KEY:
                self.send_error_response(500, 'GEMINI_API_KEY no configurada')
                return
            
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
            
            # Obtener información adicional
            info_adicional = {}
            destino_para_info = destino_detectado or destino_sesion or (destinos[0] if destinos else None)
            
            if destino_para_info:
                tipo_cambio = obtener_tipo_cambio('USD', 'EUR')
                if tipo_cambio:
                    info_adicional['tipo_cambio'] = tipo_cambio
                
                diferencia_horaria = obtener_diferencia_horaria(destino_para_info)
                if diferencia_horaria:
                    info_adicional['diferencia_horaria'] = diferencia_horaria
            
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
            
            self.send_success_response(respuesta_json)
        
        except Exception as e:
            self.send_error_response(500, f'Error al procesar: {str(e)}')
    
    def send_success_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'error': message}).encode('utf-8'))

