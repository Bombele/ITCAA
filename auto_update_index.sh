#!/bin/bash
# Script combiné de mise à jour incrémentale de l'index ITCAA
# Usage : ./auto_update_index.sh
# Peut être lancé manuellement, via cron ou CI/CD

set -euo pipefail  # stoppe en cas d'erreur, variables non définies, ou pipe cassé

LOGDIR="logs"
LOGFILE="$LOGDIR/auto_update_index_$(date +'%Y%m%d_%H%M%S').log"
MAX_LOGS=7

mkdir -p "$LOGDIR"

echo "🚀 [$(date)] Début de la mise à jour incrémentale de l'index FAISS..." | tee -a "$LOGFILE"

# Activer l'environnement virtuel si présent
if [ -d ".venv" ]; then
  source .venv/bin/activate
elif [ -d "venv" ]; then
  source venv/bin/activate
elif [ -d "ENV" ]; then
  source ENV/bin/activate
else
  echo "⚠️ Aucun environnement virtuel détecté, utilisation de Python global." | tee -a "$LOGFILE"
fi

# Vérifier que Python est disponible
if ! command -v python &> /dev/null; then
  echo "❌ Python introuvable. Abandon." | tee -a "$LOGFILE"
  exit 1
fi

# Vérifier que le module index_builder existe
if ! python -c "import importlib.util; exit(0 if importlib.util.find_spec('src.itcaa_ai_offline.data.corpus.index_builder') else 1)"; then
  echo "❌ Module index_builder introuvable. Vérifiez votre PYTHONPATH." | tee -a "$LOGFILE"
  exit 1
fi

# Lancer la mise à jour incrémentale
if python -m src.itcaa_ai_offline.data.corpus.index_builder --incremental >> "$LOGFILE" 2>&1; then
  echo "✅ [$(date)] Index FAISS mis à jour avec les nouveaux fichiers corpus." | tee -a "$LOGFILE"
else
  echo "❌ [$(date)] Échec de la mise à jour incrémentale." | tee -a "$LOGFILE"
  exit 1
fi

# Rotation des logs : conserver uniquement les $MAX_LOGS derniers
ls -t "$LOGDIR"/auto_update_index_*.log | tail -n +$((MAX_LOGS+1)) | xargs -r rm --

echo "🧹 Rotation des logs effectuée, seuls les $MAX_LOGS derniers sont conservés." | tee -a "$LOGFILE"
