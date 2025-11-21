# Configuración de Gunicorn para producción
import multiprocessing
import os

# Número de workers (recomendado: 2-4 x número de CPUs)
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))

# Bind
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"

# Timeout
timeout = 120

# Logging
accesslog = '-'
errorlog = '-'
loglevel = os.getenv('LOG_LEVEL', 'info')

# Worker class
worker_class = 'sync'

# Preload app
preload_app = True

# Max requests (para prevenir memory leaks)
max_requests = 1000
max_requests_jitter = 50

