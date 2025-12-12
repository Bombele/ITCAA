# src/itcaa_ai_offline/__init__.py
from __future__ import annotations

from pathlib import Path
from typing import Optional

# Import interne corrigé : utiliser le chemin relatif
# Si "corpus/index.py" existe, on importe directement la fonction
try:
    from .data.corpus.index_builder import build_index, load_index
except ImportError:
    # Fallback si le module n'est pas disponible
    build_index = None  # type: ignore
    load_index = None  # type: ignore


# Exemple de variable qui peut être None → annotée en Optional[str]
INDEX_PATH: Optional[str] = None


def get_index_path() -> Path:
    """
    Retourne le chemin de l'index FAISS.
    Si INDEX_PATH est None, retourne un chemin par défaut.
    """
    if INDEX_PATH is None:
        return Path("build/index.faiss")
    return Path(INDEX_PATH)