#!/bin/bash
set -euo pipefail

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

echo "🧪 Lancement des tests..."

if [ -d "tests" ]; then
    pytest tests/ \
        --cov=src/itcaa_ai_offline \
        --cov-report=xml \
        --cov-report=term-missing \
        | tee "$LOG_DIR/pytest.log"
else
    echo "❌ Dossier tests/ introuvable. Abandon."
    exit 1
fi

if [ -f coverage.xml ]; then
    echo "✅ Rapport de couverture généré : coverage.xml"
else
    echo "❌ Rapport de couverture introuvable"
    exit 1
fi
