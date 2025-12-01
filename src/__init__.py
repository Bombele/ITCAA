# src/__init__.py
"""
ITCAA Offline AI Package
========================
Ce package fournit les composants nécessaires pour :
- La prédiction IA hors ligne (Torch, FAISS, Transformers)
- La gestion des schémas Pydantic pour l’API FastAPI
- La journalisation et l’auditabilité des prédictions
- Les routes REST pour l’intégration institutionnelle

Auditabilité et robustesse intégrées pour CI/CD.
"""

__version__ = "1.0.0"
__author__ = "ITCAA Project Team"
__license__ = "MIT"

# Exposition des modules principaux
from .schemas import PredictionInput, PredictionOutput
from .predictor import OfflinePredictor
from .utils import normalize_features, log_prediction
from .routers import router

__all__ = [
    "PredictionInput",
    "PredictionOutput",
    "OfflinePredictor",
    "normalize_features",
    "log_prediction",
    "router",
]
