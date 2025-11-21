# 📸 Configuración de Unsplash API - Guía Completa

## ¿Qué es Unsplash?

Unsplash es una plataforma de fotos de alta calidad de uso libre. Su API permite buscar y obtener fotos hermosas de cualquier destino, perfecto para mostrar imágenes atractivas en tu aplicación de viajes.

---

## 📝 Cómo Obtener tu API Key Gratuita

### Paso 1: Crear una Cuenta de Desarrollador

1. Ve a [https://unsplash.com/developers](https://unsplash.com/developers)
2. Haz clic en **"Register as a developer"** o **"Get started"**
3. Inicia sesión con tu cuenta de Unsplash (o créala si no tienes una)
4. Acepta los términos de uso

### Paso 2: Crear una Aplicación

1. Una vez registrado, ve a tu **Dashboard**
2. Haz clic en **"New Application"**
3. Completa el formulario:
   - **Application name**: ViajeIA (o el nombre que prefieras)
   - **Description**: Aplicación de asistente de viajes
   - **Website URL**: http://localhost:3000 (para desarrollo)
   - Acepta los términos de uso
4. Haz clic en **"Create application"**

### Paso 3: Obtener tu Access Key

1. Una vez creada la aplicación, verás tu **Access Key** y **Secret Key**
2. **Copia el Access Key** - este es el que necesitas
3. El Access Key se ve así: `tu_access_key_aqui`

### Paso 4: Configurar en tu Proyecto

1. Abre el archivo `backend/.env`
2. Agrega esta línea:
   ```env
   UNSPLASH_ACCESS_KEY=tu_access_key_aqui
   ```
3. Reemplaza `tu_access_key_aqui` con tu Access Key real
4. Guarda el archivo
5. **Reinicia el backend** para que cargue la nueva variable

---

## 🆓 Plan Gratuito - Límites

El plan gratuito de Unsplash incluye:

- ✅ **50 solicitudes por hora**
- ✅ **5,000 solicitudes por mes**
- ✅ **Acceso completo a la biblioteca de fotos**
- ✅ **Fotos de alta calidad**
- ✅ **Sin marca de agua**

**Nota:** Para proyectos con más tráfico, considera actualizar a un plan de pago.

---

## 🔧 Verificar que Funciona

### Opción 1: Probar desde el Código

Ejecuta este script de prueba:

```bash
cd backend
.\venv\Scripts\activate.ps1
python -c "import os; from dotenv import load_dotenv; load_dotenv(); import requests; key = os.getenv('UNSPLASH_ACCESS_KEY'); print('Access Key:', key[:20] + '...' if key else 'NO CONFIGURADA'); headers = {'Authorization': f'Client-ID {key}'}; r = requests.get('https://api.unsplash.com/search/photos', headers=headers, params={'query': 'Paris', 'per_page': 1}); print('Status:', r.status_code); print('Fotos encontradas:', len(r.json()['results']) if r.status_code == 200 else 0)"
```

### Opción 2: Probar desde el Navegador

Abre esta URL en tu navegador (reemplaza `TU_ACCESS_KEY`):

```
https://api.unsplash.com/search/photos?query=Paris&per_page=3&client_id=TU_ACCESS_KEY
```

Deberías ver un JSON con información de fotos.

---

## 🚀 Cómo Funciona en ViajeIA

Una vez configurada la API Key:

1. **El usuario pregunta sobre un destino** (ej: "Quiero viajar a París")
2. **El sistema detecta automáticamente** el nombre de la ciudad
3. **Se buscan 3 fotos hermosas** del destino usando Unsplash
4. **Las fotos se muestran automáticamente** en una galería elegante cuando Axl responde

### Características de las Fotos:

- ✅ **3 fotos por destino** seleccionadas automáticamente
- ✅ **Fotos en formato landscape** (apaisadas) para mejor visualización
- ✅ **Ordenadas por popularidad** (las más hermosas primero)
- ✅ **Créditos al fotógrafo** (hover sobre la foto)
- ✅ **Carga lazy** para mejor rendimiento

---

## ⚠️ Solución de Problemas

### Error: "Unauthorized" o 401
- Verifica que copiaste el **Access Key** correctamente (no el Secret Key)
- Asegúrate de que no hay espacios antes o después
- Verifica que el archivo `.env` está en `backend/.env`

### Error: "Rate limit exceeded"
- Has alcanzado el límite de 50 solicitudes por hora
- Espera un momento o considera actualizar tu plan

### Las fotos no aparecen
- Verifica que `UNSPLASH_ACCESS_KEY` está en `backend/.env`
- Reinicia el backend después de agregar la variable
- Revisa los logs del backend para ver errores
- Asegúrate de que el destino se detecta correctamente

### Fotos genéricas o no relacionadas
- Algunos destinos pueden tener nombres ambiguos
- El sistema busca automáticamente, pero puedes mejorar los resultados usando nombres más específicos

---

## 📚 Recursos Adicionales

- **Documentación oficial**: [https://unsplash.com/documentation](https://unsplash.com/documentation)
- **Dashboard de desarrollador**: [https://unsplash.com/developers](https://unsplash.com/developers)
- **Términos de uso**: [https://unsplash.com/api-terms](https://unsplash.com/api-terms)

---

## ✅ Checklist de Configuración

- [ ] Cuenta creada en Unsplash Developers
- [ ] Aplicación creada en el dashboard
- [ ] Access Key obtenida
- [ ] Access Key agregada a `backend/.env`
- [ ] Backend reiniciado
- [ ] Probado con una pregunta sobre un destino
- [ ] Las fotos aparecen en la galería

---

## 💡 Tips

- **Usa nombres específicos**: "París, Francia" funciona mejor que solo "París"
- **Nombres en inglés**: Algunos destinos funcionan mejor con nombres en inglés
- **Ciudades populares**: Las ciudades más turísticas tienen más fotos disponibles

---

¡Listo! Ahora Axl mostrará automáticamente 3 fotos hermosas de cada destino cuando responda. 📸✈️

