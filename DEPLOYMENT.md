# Guía de Despliegue - ViajeIA

Esta guía te ayudará a desplegar ViajeIA en un servidor de producción.

## 📋 Requisitos Previos

- Servidor Linux (Ubuntu 20.04+ recomendado)
- Python 3.8+
- Node.js 16+ y npm
- Nginx
- Certificado SSL (Let's Encrypt recomendado)
- Dominio configurado apuntando a tu servidor

---

## 🚀 Instrucciones para Localhost (Desarrollo)

### Backend

1. **Navega a la carpeta backend:**
   ```bash
   cd backend
   ```

2. **Crea un entorno virtual:**
   ```bash
   python -m venv venv
   ```

3. **Activa el entorno virtual:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configura las variables de entorno:**
   ```bash
   # Copia el archivo de ejemplo
   cp .env.example .env
   
   # Edita .env y agrega tu API key
   # GEMINI_API_KEY=tu_api_key_aqui
   ```

6. **Ejecuta el servidor:**
   ```bash
   python app.py
   ```

El backend estará disponible en `http://localhost:5000`

### Frontend

1. **Navega a la carpeta frontend:**
   ```bash
   cd frontend
   ```

2. **Instala las dependencias:**
   ```bash
   npm install
   ```

3. **Configura las variables de entorno:**
   ```bash
   # El archivo .env.development ya está configurado para localhost
   # Si necesitas cambiarlo, edita .env.development
   ```

4. **Ejecuta la aplicación:**
   ```bash
   npm start
   ```

El frontend estará disponible en `http://localhost:3000`

---

## 🌐 Instrucciones para Producción

### 1. Preparar el Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx
sudo apt install -y nodejs npm
```

### 2. Configurar el Backend

```bash
# Crear directorio para la aplicación
sudo mkdir -p /var/www/viajeia
sudo chown $USER:$USER /var/www/viajeia

# Clonar o copiar tu proyecto
cd /var/www/viajeia

# Configurar backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
nano .env  # Edita y configura tus variables
```

**Configuración de `.env` para producción:**
```env
GEMINI_API_KEY=tu_api_key_aqui
PORT=5000
FLASK_DEBUG=False
ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com
```

### 3. Configurar el Frontend

```bash
cd /var/www/viajeia/frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env.production
nano .env.production  # Cambia la URL del API
```

**Configuración de `.env.production`:**
```env
REACT_APP_API_URL=https://api.tudominio.com
# O si usas el mismo dominio:
REACT_APP_API_URL=https://tudominio.com
```

```bash
# Construir para producción
npm run build
```

### 4. Configurar Gunicorn (Servidor WSGI)

```bash
cd /var/www/viajeia/backend
source venv/bin/activate

# Probar Gunicorn manualmente
gunicorn -c gunicorn_config.py wsgi:app
```

### 5. Crear Servicio Systemd para el Backend

```bash
sudo nano /etc/systemd/system/viajeia.service
```

Contenido del archivo:
```ini
[Unit]
Description=ViajeIA Backend Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/viajeia/backend
Environment="PATH=/var/www/viajeia/backend/venv/bin"
ExecStart=/var/www/viajeia/backend/venv/bin/gunicorn -c gunicorn_config.py wsgi:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar y iniciar el servicio
sudo systemctl daemon-reload
sudo systemctl enable viajeia
sudo systemctl start viajeia
sudo systemctl status viajeia
```

### 6. Configurar Nginx

```bash
# Copiar configuración de ejemplo
sudo cp /var/www/viajeia/nginx.conf.example /etc/nginx/sites-available/viajeia

# Editar configuración
sudo nano /etc/nginx/sites-available/viajeia
# Cambia 'tudominio.com' por tu dominio real

# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/viajeia /etc/nginx/sites-enabled/

# Probar configuración
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

### 7. Configurar SSL con Let's Encrypt

```bash
# Obtener certificado SSL
sudo certbot --nginx -d tudominio.com -d www.tudominio.com

# Renovación automática (ya está configurado por defecto)
sudo certbot renew --dry-run
```

### 8. Configurar Firewall

```bash
# Permitir HTTP, HTTPS y SSH
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

---

## 🔒 Seguridad Adicional

### 1. Variables de Entorno

**NUNCA** subas archivos `.env` a Git. Ya están en `.gitignore`.

### 2. Permisos de Archivos

```bash
# Backend
sudo chown -R www-data:www-data /var/www/viajeia/backend
sudo chmod -R 755 /var/www/viajeia/backend

# Frontend
sudo chown -R www-data:www-data /var/www/viajeia/frontend
sudo chmod -R 755 /var/www/viajeia/frontend
```

### 3. Actualizar Dependencias Regularmente

```bash
# Backend
cd /var/www/viajeia/backend
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Frontend
cd /var/www/viajeia/frontend
npm update
npm audit fix
```

### 4. Monitoreo y Logs

```bash
# Ver logs del backend
sudo journalctl -u viajeia -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

---

## 🔄 Actualizar la Aplicación

```bash
# 1. Detener servicios
sudo systemctl stop viajeia

# 2. Actualizar código (git pull, etc.)

# 3. Backend
cd /var/www/viajeia/backend
source venv/bin/activate
pip install -r requirements.txt

# 4. Frontend
cd /var/www/viajeia/frontend
npm install
npm run build

# 5. Reiniciar servicios
sudo systemctl restart viajeia
sudo systemctl restart nginx
```

---

## 🐛 Solución de Problemas

### El backend no inicia
```bash
# Ver logs
sudo journalctl -u viajeia -n 50

# Verificar variables de entorno
cd /var/www/viajeia/backend
source venv/bin/activate
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
```

### Error 502 Bad Gateway
- Verifica que el backend esté corriendo: `sudo systemctl status viajeia`
- Verifica el puerto en la configuración de Nginx
- Revisa los logs: `sudo journalctl -u viajeia -f`

### CORS Errors
- Verifica `ALLOWED_ORIGINS` en `.env` del backend
- Asegúrate de incluir tu dominio con `https://`

### Frontend no carga
- Verifica que `npm run build` se ejecutó correctamente
- Verifica permisos en `/var/www/viajeia/frontend/build`
- Revisa logs de Nginx: `sudo tail -f /var/log/nginx/error.log`

---

## 📝 Checklist de Despliegue

- [ ] Servidor actualizado y configurado
- [ ] Backend instalado y configurado con variables de entorno
- [ ] Frontend construido para producción
- [ ] Gunicorn configurado y funcionando
- [ ] Servicio systemd creado y activo
- [ ] Nginx configurado correctamente
- [ ] SSL configurado con Let's Encrypt
- [ ] Firewall configurado
- [ ] Permisos de archivos correctos
- [ ] Variables de entorno seguras (no en Git)
- [ ] Logs monitoreados
- [ ] Pruebas de funcionalidad completadas

---

## 📞 Soporte

Si encuentras problemas, revisa los logs y verifica cada paso de la configuración.

