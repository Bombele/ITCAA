# src/itcaa_ai_offline/models/loader.py
from __future__ import annotations

from pathlib import Path
from typing import Optional, Dict, Any, List


# Exemple de variable qui peut être None → annotée en Optional[str]
MODEL_PATH: Optional[str] = None


def load_model(path: Optional[str] = None) -> Dict[str, Any]:
    """
    Charge un modèle depuis un chemin donné.
    Si aucun chemin n'est fourni, utilise MODEL_PATH ou un chemin par défaut.
    """
    model_path: str
    if path is not None:
        model_path = path
    elif MODEL_PATH is not None:
        model_path = MODEL_PATH
    else:
        model_path = "build/model.json"

    # Lecture du fichier
    with open(model_path, "r", encoding="utf-8") as f:
        # Exemple : retourne un dict factice
        return {"path": model_path, "content": f.read()}


def list_available_models(directory: str = "build/models") -> List[str]:
    """
    Retourne la liste des modèles disponibles dans un répertoire.
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return []
    return [p.name for p in dir_path.glob("*.json")]