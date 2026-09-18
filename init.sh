#!/usr/bin/env bash
set -euo pipefail

# Inicializador del proyecto MateBursatil
# - Crea y activa un virtualenv en `.venv` (si no existe)
# - Instala `requirements.txt` (si existe)
# - Ejecuta el scraper para generar `data/cotizaciones.json`
# - Arranca la API FastAPI con uvicorn

VENV_DIR=".venv"

echo "Usando directorio de virtualenv: $VENV_DIR"

if [ ! -d "$VENV_DIR" ]; then
  echo "Creando virtualenv en $VENV_DIR..."
  python3 -m venv "$VENV_DIR"
fi

echo "Activando virtualenv..."
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

if [ -f "requirements.txt" ]; then
  echo "Instalando dependencias desde requirements.txt..."
  pip install --upgrade pip
  pip install -r requirements.txt
fi

echo "Asegurando existencia de carpeta data/"
mkdir -p data

echo "Ejecutando scraper para generar data/cotizaciones.json..."
python services/scraper.py

echo "Iniciando FastAPI (uvicorn) en 0.0.0.0:8000"
# Ejecuta en primer plano para que el script muestre los logs.
uvicorn api.main:app --host 0.0.0.0 --port 8000
