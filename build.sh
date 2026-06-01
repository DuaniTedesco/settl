#!/usr/bin/env bash
set -e

echo "==> Instalando dependências..."
pip install -r requirements.txt

echo "==> Rodando migrations..."
python manage.py migrate --no-input

echo "==> Coletando static files..."
python manage.py collectstatic --no-input

echo "==> Build concluído!"
