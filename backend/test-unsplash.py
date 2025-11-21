"""
Script para probar la API de Unsplash
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

UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY', '')
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY', '')

api_key = UNSPLASH_ACCESS_KEY or UNSPLASH_API_KEY

if not api_key:
    print("❌ UNSPLASH_ACCESS_KEY o UNSPLASH_API_KEY no está configurada en .env")
    print("\nPara obtener una API key gratuita:")
    print("1. Ve a https://unsplash.com/developers")
    print("2. Crea una cuenta o inicia sesión")
    print("3. Crea una nueva aplicación")
    print("4. Copia el 'Access Key'")
    print("5. Agrégalo a backend/.env como: UNSPLASH_ACCESS_KEY=tu_access_key")
    sys.exit(1)

print(f"✅ API Key encontrada: {api_key[:15]}...")

# Probar con varios destinos
destinos_prueba = ['Paris', 'Barcelona', 'Tokyo', 'New York', 'Bali']

for destino in destinos_prueba:
    print(f"\n📸 Probando con: {destino}")
    try:
        url = "https://api.unsplash.com/search/photos"
        headers = {
            'Authorization': f'Client-ID {api_key}'
        }
        params = {
            'query': destino,
            'per_page': 3,
            'orientation': 'landscape',
            'order_by': 'popularity'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                print(f"   ✅ Éxito! {len(data['results'])} fotos encontradas")
                for i, foto in enumerate(data['results'][:3], 1):
                    print(f"   Foto {i}:")
                    print(f"      URL: {foto['urls']['regular'][:60]}...")
                    print(f"      Autor: {foto['user']['name']}")
                    print(f"      Descripción: {foto.get('description', 'N/A')[:50]}")
            else:
                print(f"   ⚠️ No se encontraron resultados")
        elif response.status_code == 401:
            print(f"   ❌ Error 401: API Key inválida o no autorizada")
        elif response.status_code == 403:
            print(f"   ❌ Error 403: Acceso denegado - verifica tu API key")
        else:
            print(f"   ❌ Error {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Excepción: {str(e)}")

print("\n" + "="*50)
print("Prueba completada")

