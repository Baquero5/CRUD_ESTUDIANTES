#!/bin/bash

# Script de entrada para el contenedor Django

echo "🚀 Iniciando aplicación Django..."

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando a PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "✅ PostgreSQL está listo!"

# Aplicar migraciones
echo "📦 Aplicando migraciones..."
python manage.py migrate --noinput

# Crear superusuario si no existe
echo "👤 Verificando superusuario..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@ejemplo.com', 'admin123')
    print('✅ Superusuario creado: admin/admin123')
else:
    print('ℹ️  Superusuario ya existe')
END

# Recolectar archivos estáticos
echo "📂 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✨ Aplicación lista!"

# Ejecutar el comando pasado al contenedor
exec "$@"