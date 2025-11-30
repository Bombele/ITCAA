# src/itcaa_ai_offline/__init__.py

# Import explicite des sous-modules
from . import config
from .data.corpus import index_builder
# Vérifie que predictor existe avant de l'importer
try:
    from . import predictor
except ImportError:
    predictor = None

# Définition de l'API publique
__all__ = ["config", "index_builder", "predictor"]
