# 🚀 Cómo Iniciar ViajeIA

## Opción 1: Iniciar Todo Automáticamente (Recomendado)

Ejecuta desde la **raíz del proyecto**:

```powershell
.\start-all.ps1
```

Esto abrirá:
- ✅ Una ventana nueva para el **Backend** (puerto 5000)
- ✅ Una ventana nueva para el **Frontend** (puerto 3000)
- ✅ El navegador se abrirá automáticamente

---

## Opción 2: Iniciar Manualmente (Paso a Paso)

### Paso 1: Backend (Terminal 1)

Abre una terminal PowerShell y ejecuta:

```powershell
.\start-backend.ps1
```

Espera a ver: `* Running on http://127.0.0.1:5000`

### Paso 2: Frontend (Terminal 2)

Abre **otra** terminal PowerShell (nueva ventana) y ejecuta:

```powershell
.\start-frontend.ps1
```

O manualmente:
```powershell
cd frontend
npm start
```

El navegador se abrirá automáticamente en `http://localhost:3000`

---

## ✅ Verificar que Todo Funciona

1. **Backend**: Abre `http://localhost:5000/api/health` en tu navegador
   - Deberías ver: `{"status":"ok","service":"ViajeIA API"}`

2. **Frontend**: Abre `http://localhost:3000`
   - Deberías ver la aplicación ViajeIA con el formulario inicial

---

## ❓ Problemas Comunes

### "No se abren nuevas ventanas"
- Ejecuta `start-backend.ps1` y `start-frontend.ps1` manualmente en terminales separadas
- O usa la Opción 2 arriba

### "ERR_CONNECTION_REFUSED en localhost:3000"
- El frontend no está corriendo
- Ejecuta `.\start-frontend.ps1` en una nueva terminal

### "ERR_CONNECTION_REFUSED en localhost:5000"
- El backend no está corriendo
- Ejecuta `.\start-backend.ps1` en una nueva terminal

---

## 📝 Nota Importante

**Mantén ambas terminales abiertas** mientras uses la aplicación:
- Terminal 1: Backend (debe seguir corriendo)
- Terminal 2: Frontend (debe seguir corriendo)

Si cierras alguna terminal, ese servidor se detendrá.

