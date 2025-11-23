# 🔧 Solución de Errores Comunes - ViajeIA

## Error: ERR_CONNECTION_REFUSED

Este error significa que el **backend no está corriendo** o no está accesible en `http://localhost:5000`.

### ✅ Solución Rápida

**Opción 1: Iniciar todo automáticamente**
```powershell
.\start-all.ps1
```

**Opción 2: Iniciar por separado**

1. **Terminal 1 - Backend:**
   ```powershell
   .\start-backend.ps1
   ```
   Espera a ver: `* Running on http://127.0.0.1:5000`

2. **Terminal 2 - Frontend:**
   ```powershell
   .\start-frontend.ps1
   ```
   O manualmente:
   ```powershell
   cd frontend
   npm start
   ```

### 🔍 Verificar que el Backend está Corriendo

1. Abre tu navegador y ve a: `http://localhost:5000/api/health`
2. Deberías ver: `{"status":"ok","service":"ViajeIA API"}`
3. Si ves un error, el backend no está corriendo

### 📝 Checklist

- [ ] Backend corriendo en `http://localhost:5000`
- [ ] Frontend corriendo en `http://localhost:3000`
- [ ] Archivo `backend/.env` existe y tiene la API key
- [ ] Archivo `frontend/.env.development` existe con `REACT_APP_API_URL=http://localhost:5000`

---

## Error: "Error con la API de Gemini"

Este error significa que hay un problema con la API key o el modelo de Gemini.

### ✅ Solución

1. Verifica que `backend/.env` tiene:
   ```env
   GEMINI_API_KEY=AIzaSyBgtKCWZ7IbPujHbfCuCihRfXW3B3VMsb4
   GEMINI_MODEL=gemini-2.0-flash
   ```

2. Reinicia el backend después de cambiar el `.env`

3. Prueba la conexión:
   ```powershell
   cd backend
   .\venv\Scripts\activate.ps1
   python test-gemini.py
   ```

---

## Error: UnicodeDecodeError al iniciar backend

Este error es por codificación incorrecta del archivo `.env`.

### ✅ Solución

El script `start-backend.ps1` ahora recrea el archivo automáticamente. Si persiste:

1. Elimina `backend/.env`
2. Ejecuta `.\start-backend.ps1` de nuevo
3. El archivo se recreará con codificación UTF-8 correcta

---

## Error: "Module not found"

### ✅ Solución

**Backend:**
```powershell
cd backend
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
```

**Frontend:**
```powershell
cd frontend
npm install
```

---

## El Backend se Inicia pero se Detiene Inmediatamente

### ✅ Solución

1. Verifica que el archivo `.env` existe y tiene formato correcto
2. Revisa la ventana de PowerShell para ver el error exacto
3. Asegúrate de que el puerto 5000 no esté en uso:
   ```powershell
   netstat -ano | findstr :5000
   ```

---

## Ayuda Adicional

Si ningún error de arriba aplica, comparte:
1. El mensaje de error completo de la consola del navegador
2. El mensaje de error de la terminal donde corre el backend
3. Una captura de pantalla si es posible

