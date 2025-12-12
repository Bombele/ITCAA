# src/itcaa_ai_offline/models/__init__.py
from __future__ import annotations

from typing import Optional

# Corriger l'import : utiliser le chemin relatif vers capsules.py
try:
    from .capsules import Capsule
except ImportError:
    Capsule = None  # type: ignore


# Exemple de variable qui peut être None → annotée en Optional[str]
MODEL_PATH: Optional[str] = None


def get_model_path() -> str:
    """
    Retourne le chemin du modèle.
    Si MODEL_PATH est None, retourne un chemin par défaut.
    """
    if MODEL_PATH is None:
        return "build/model.json"
    return MODEL_PATH
