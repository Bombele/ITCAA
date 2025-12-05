#!/bin/bash
# Script de vérification du linting et du typage Python
# Usage : ./link_check.sh

set -euo pipefail  # stoppe en cas d'erreur, variables non définies, ou pipe cassé

LOGDIR="logs"
LOGFILE="$LOGDIR/lint_check_$(date +'%Y%m%d_%H%M%S').log"
MAX_LOGS=7

mkdir -p "$LOGDIR"

echo "🔍 [$(date)] Début des vérifications de linting et typage..." | tee -a "$LOGFILE"

# Vérifier que les outils sont installés
for tool in black isort mypy; do
  if ! command -v $tool &> /dev/null; then
    echo "❌ Outil $tool introuvable. Installez-le avec 'pip install $tool'." | tee -a "$LOGFILE"
    exit 1
  fi
done

# Vérification Black
echo "🔍 Vérification Black..." | tee -a "$LOGFILE"
if ! black --check src/ tests/ >> "$LOGFILE" 2>&1; then
  echo "❌ Black a trouvé des erreurs" | tee -a "$LOGFILE"
  exit 1
else
  echo "✅ Black OK" | tee -a "$LOGFILE"
fi

# Vérification Isort
echo "🔍 Vérification Isort..." | tee -a "$LOGFILE"
if ! isort --check-only src/ tests/ >> "$LOGFILE" 2>&1; then
  echo "❌ Isort a trouvé des erreurs" | tee -a "$LOGFILE"
  exit 1
else
  echo "✅ Isort OK" | tee -a "$LOGFILE"
fi

# Vérification Mypy
echo "🔍 Vérification Mypy..." | tee -a "$LOGFILE"
if ! mypy src/ >> "$LOGFILE" 2>&1; then
  echo "❌ Mypy a trouvé des erreurs" | tee -a "$LOGFILE"
  exit 1
else
  echo "✅ Mypy OK" | tee -a "$LOGFILE"
fi

echo "🎉 [$(date)] Toutes les vérifications sont passées avec succès." | tee -a "$LOGFILE"

# Rotation des logs : conserver uniquement les $MAX_LOGS derniers
ls -t "$LOGDIR"/lint_check_*.log | tail -n +$((MAX_LOGS+1)) | xargs -r rm --

echo "🧹 Rotation des logs effectuée, seuls les $MAX_LOGS derniers sont conservés." | tee -a "$LOGFILE"
