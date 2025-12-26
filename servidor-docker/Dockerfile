FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para weasyprint, lxml y compilación
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential \
	   gcc \
	   pkg-config \
	   libxml2-dev libxslt1-dev zlib1g-dev \
	   libffi-dev libjpeg-dev libpng-dev \
	   libcairo2 libcairo2-dev \
	libpango-1.0-0 libpango1.0-dev \
	libgdk-pixbuf-xlib-2.0-0 \
	   libgirepository1.0-dev gir1.2-pango-1.0 \
	   python3-dev \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar e instalar requerimientos Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto completo
COPY . .

# Configurar variables de entorno
ENV PYTHONPATH=/app
ENV FLASK_APP=servidor-docker/app.py

# Exponer el puerto
EXPOSE 5000

# Ejecutar la aplicación con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "servidor-docker.app:app"]