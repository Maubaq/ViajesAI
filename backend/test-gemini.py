"""
Script de prueba para verificar la conexión con Gemini API
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

# Configurar API Key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ Error: GEMINI_API_KEY no está configurada en .env")
    exit(1)

print(f"✅ API Key encontrada: {api_key[:20]}...")

# Configurar Gemini
genai.configure(api_key=api_key)

# Probar diferentes modelos
modelos_a_probar = [
    'gemini-2.0-flash-exp',
    'gemini-2.0-flash',
    'gemini-1.5-flash',
    'gemini-pro'
]

print("\n🔍 Probando modelos disponibles...\n")

for modelo_nombre in modelos_a_probar:
    try:
        print(f"Probando: {modelo_nombre}...", end=" ")
        model = genai.GenerativeModel(modelo_nombre)
        response = model.generate_content("Di hola en una palabra")
        print(f"✅ FUNCIONA - Respuesta: {response.text}")
        print(f"   → Este modelo está disponible y funcionando\n")
        break
    except Exception as e:
        print(f"❌ Error: {str(e)[:100]}\n")

print("\n✅ Prueba completada")

