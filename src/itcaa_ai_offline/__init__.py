"""
ITCAA Offline Package
Ce module regroupe les utilitaires principaux :
- config : chemins et paramètres
- index_builder : construction et mise à jour de l'index FAISS
- predictor : prédiction (si disponible)
"""

from . import config
from .data.corpus.index_builder import build_index
from repair_index import check_and_repair_index

# Vérifie que predictor existe avant de l'importer
try:
    from . import predictor
except ImportError:
    predictor = None

# API publique
__all__ = [
    "config",
    "build_index",
    "check_and_repair_index",
    "predictor",
]
