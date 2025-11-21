# 🌤️ Configuración de Weatherbit API - Guía Completa

## ¿Qué es Weatherbit?

Weatherbit es una API de datos meteorológicos que proporciona información del clima actual y pronósticos. Ofrece un plan **gratuito** con límites generosos para uso personal y proyectos pequeños.

---

## 📝 Cómo Obtener tu API Key Gratuita

### Paso 1: Crear una Cuenta

1. Ve a [https://www.weatherbit.io/](https://www.weatherbit.io/)
2. Haz clic en **"Sign Up"** o **"Get Started"** (arriba a la derecha)
3. Completa el formulario de registro:
   - Email
   - Contraseña
   - Nombre
4. Verifica tu email (revisa tu bandeja de entrada)

### Paso 2: Obtener tu API Key

1. Una vez registrado, inicia sesión
2. Ve a tu **Dashboard** o **Account Settings**
3. Busca la sección **"API Keys"** o **"My API Keys"**
4. Verás tu API Key (una cadena de caracteres alfanuméricos)
5. **Copia tu API Key** - la necesitarás en el siguiente paso

### Paso 3: Configurar en tu Proyecto

1. Abre el archivo `backend/.env`
2. Agrega esta línea:
   ```env
   WEATHERBIT_API_KEY=tu_api_key_aqui
   ```
3. Reemplaza `tu_api_key_aqui` con tu API Key real
4. Guarda el archivo
5. **Reinicia el backend** para que cargue la nueva variable

---

## 🆓 Plan Gratuito - Límites

El plan gratuito de Weatherbit incluye:

- ✅ **500 llamadas por día**
- ✅ **Clima actual** (Current Weather)
- ✅ **Pronósticos de 16 días**
- ✅ **Datos históricos** (limitados)
- ✅ **Soporte para múltiples idiomas** (incluyendo español)

**Nota:** Para proyectos con más tráfico, considera actualizar a un plan de pago.

---

## 🔧 Verificar que Funciona

### Opción 1: Probar desde el Código

Ejecuta este script de prueba:

```bash
cd backend
.\venv\Scripts\activate.ps1
python -c "import os; from dotenv import load_dotenv; load_dotenv(); import requests; key = os.getenv('WEATHERBIT_API_KEY'); print('API Key:', key[:20] + '...' if key else 'NO CONFIGURADA'); r = requests.get('https://api.weatherbit.io/v2.0/current', params={'city': 'Paris', 'key': key}); print('Status:', r.status_code); print('Clima:', r.json() if r.status_code == 200 else 'Error')"
```

### Opción 2: Probar desde el Navegador

Abre esta URL en tu navegador (reemplaza `TU_API_KEY`):

```
https://api.weatherbit.io/v2.0/current?city=Paris&key=TU_API_KEY
```

Deberías ver un JSON con información del clima.

---

## 🚀 Cómo Funciona en ViajeIA

Una vez configurada la API Key:

1. **El usuario pregunta sobre un destino** (ej: "Quiero viajar a París")
2. **El sistema detecta automáticamente** el nombre de la ciudad
3. **Se consulta el clima actual** de esa ciudad usando Weatherbit
4. **Axl incluye la información del clima** en su respuesta, con recomendaciones sobre:
   - Qué ropa llevar
   - Actividades apropiadas para el clima
   - Condiciones actuales del destino

### Ejemplo de Respuesta de Axl:

```
¡Hola! Soy Axl, tu consultor personal de viajes 🧳

**Clima actual en París:**
🌡️ Temperatura: 15°C
🌤️ Condiciones: Cielo despejado
💧 Humedad: 65%

**Recomendaciones:**
• Lleva una chaqueta ligera, el clima está fresco
• Perfecto para caminar por la ciudad
• Las noches pueden ser más frías, trae algo abrigado
```

---

## ⚠️ Solución de Problemas

### Error: "API key not valid"
- Verifica que copiaste la API Key correctamente
- Asegúrate de que no hay espacios antes o después
- Verifica que el archivo `.env` está en `backend/.env`

### Error: "Rate limit exceeded"
- Has alcanzado el límite de 500 llamadas por día
- Espera hasta el día siguiente o considera actualizar tu plan

### Error: "City not found"
- Algunas ciudades pueden tener nombres diferentes en la API
- Intenta usar el nombre en inglés o el código de ciudad

### El clima no aparece en las respuestas
- Verifica que `WEATHERBIT_API_KEY` está en `backend/.env`
- Reinicia el backend después de agregar la variable
- Revisa los logs del backend para ver errores

---

## 📚 Recursos Adicionales

- **Documentación oficial**: [https://www.weatherbit.io/api](https://www.weatherbit.io/api)
- **Ejemplos de código**: [https://www.weatherbit.io/api/code-examples](https://www.weatherbit.io/api/code-examples)
- **Soporte**: [support@weatherbit.io](mailto:support@weatherbit.io)

---

## ✅ Checklist de Configuración

- [ ] Cuenta creada en Weatherbit.io
- [ ] API Key obtenida
- [ ] API Key agregada a `backend/.env`
- [ ] Backend reiniciado
- [ ] Probado con una pregunta sobre un destino
- [ ] El clima aparece en las respuestas de Axl

---

¡Listo! Ahora Axl podrá incluir información del clima actual en sus recomendaciones de viaje. 🌤️✈️

