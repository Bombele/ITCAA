#!/bin/bash
set -euo pipefail

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

echo "🔧 Installation des dépendances..."
if [ -f requirements.txt ]; then
    python -m pip install --upgrade pip | tee "$LOG_DIR/pip.log"
    pip install -r requirements.txt | tee "$LOG_DIR/requirements.log"
else
    echo "❌ Fichier requirements.txt introuvable. Abandon."
    exit 1
fi

echo "🧠 Configuration du PYTHONPATH..."
export PYTHONPATH="$(pwd):$(pwd)/src"

echo "🚀 Lancement de l'API ITCAA..."
# ⚠️ En dev → --reload ; en prod → sans reload
if [ "${ENV:-dev}" = "prod" ]; then
    uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 | tee "$LOG_DIR/uvicorn.log"
else
    uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --reload | tee "$LOG_DIR/uvicorn.log"
fi
