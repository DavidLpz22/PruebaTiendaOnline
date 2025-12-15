#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# --- AGREGA ESTA LÍNEA AL FINAL ---
# Intenta crear el superusuario. Si ya existe, imprime un mensaje y continúa sin error.
python manage.py createsuperuser --noinput || echo "El superusuario ya existe, omitiendo creación."