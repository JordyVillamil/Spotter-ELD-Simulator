# Usamos una versión ligera de Python
FROM python:3.11-slim

# Configuraciones para que Python no genere basura y los logs salgan en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Definimos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema operativo que algunas librerías de Python necesitan
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo de requerimientos PRIMERO (para aprovechar la caché de Docker)
COPY requirements.txt .

# Instalamos las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el resto del código del proyecto al contenedor
COPY . .

# Exponemos el puerto que usará Render (Render usa el 10000 por defecto)
EXPOSE 10000

# El comando maestro que arranca Gunicorn apuntando a tu carpeta spotter_api
CMD ["gunicorn", "spotter_api.wsgi:application", "--bind", "0.0.0.0:10000"]