#!/bin/bash
# Script de mise à jour incrémentale de l'index ITCAA
# Usage : ./auto_update_index.sh

set -e  # stoppe en cas d'erreur

echo "🚀 Mise à jour incrémentale de l'index FAISS..."

# Activer l'environnement virtuel si nécessaire
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

# Lancer la mise à jour incrémentale
python -m src.itcaa_ai_offline.data.corpus.index_builder --incremental

echo "✅ Index FAISS mis à jour avec les nouveaux fichiers corpus."