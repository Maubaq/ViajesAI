"""
Script para probar la API de Weatherbit
"""
import os
import sys
import requests
from pathlib import Path

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
except Exception as e:
    print(f"Advertencia: No se pudo cargar dotenv: {e}")

WEATHERBIT_API_KEY = os.getenv('WEATHERBIT_API_KEY', '')

if not WEATHERBIT_API_KEY:
    print("❌ WEATHERBIT_API_KEY no está configurada en .env")
    sys.exit(1)

print(f"✅ API Key encontrada: {WEATHERBIT_API_KEY[:10]}...")

# Probar con varias ciudades
ciudades_prueba = ['Paris', 'Barcelona', 'Madrid', 'Mexico City', 'Bogota']

for ciudad in ciudades_prueba:
    print(f"\n🌍 Probando con: {ciudad}")
    try:
        url = "https://api.weatherbit.io/v2.0/current"
        params = {
            'city': ciudad,
            'key': WEATHERBIT_API_KEY,
            'lang': 'es',
            'units': 'M'
        }
        
        response = requests.get(url, params=params, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                clima = data['data'][0]
                print(f"   ✅ Éxito!")
                print(f"   Ciudad: {clima.get('city_name', 'N/A')}")
                print(f"   Temperatura: {clima.get('temp', 'N/A')}°C")
                print(f"   Descripción: {clima.get('weather', {}).get('description', 'N/A')}")
                print(f"   Humedad: {clima.get('rh', 'N/A')}%")
            else:
                print(f"   ⚠️ Respuesta vacía")
        elif response.status_code == 403:
            print(f"   ❌ Error 403: API Key inválida o no autorizada")
            print(f"   Response: {response.text[:200]}")
        elif response.status_code == 429:
            print(f"   ⚠️ Error 429: Límite de rate alcanzado")
        else:
            print(f"   ❌ Error {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Excepción: {str(e)}")

print("\n" + "="*50)
print("Prueba completada")

