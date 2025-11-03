# Usar Python 3.10 como imagen base
FROM python:3.10-slim

# Información del mantenedor
LABEL maintainer="estudiantes-project"
LABEL description="Sistema de Gestión de Estudiantes - Django"

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt primero (para aprovechar cache de Docker)
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . /app/

# Crear directorio para archivos estáticos
RUN mkdir -p /app/staticfiles

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput || true

# Exponer el puerto 8000
EXPOSE 8000

# Crear script de entrada
RUN chmod +x /app/entrypoint.sh || true

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]