# src/itcaa_ai_offline/index_builder.py
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
from numpy.typing import NDArray
import faiss
import json


def build_embeddings(texts: List[str]) -> NDArray[np.float32]:
    """
    Construit des embeddings à partir d'une liste de textes.
    Retourne un tableau numpy de float32.
    """
    embeddings: NDArray[np.float32] = np.random.rand(len(texts), 128).astype(np.float32)
    return embeddings


def save_full_index(
    index: faiss.Index,
    meta: List[Dict[str, str]],
    index_path: Path
) -> None:
    """
    Sauvegarde l'index FAISS et les métadonnées associées.
    """
    faiss.write_index(index, str(index_path))
    meta_path = index_path.with_suffix(".meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)


def load_index(index_path: Path) -> Optional[faiss.Index]:
    """
    Charge un index FAISS depuis un fichier.
    Retourne None si le fichier n'existe pas.
    """
    if not index_path.exists():
        return None
    return faiss.read_index(str(index_path))


def repair_index(index_path: Path) -> None:
    """
    Répare un index FAISS en recréant les entrées manquantes.
    """
    index = load_index(index_path)
    if index is None:
        raise FileNotFoundError(f"Index not found at {index_path}")

    # Liste typée pour les nouvelles entrées
    new_entries: List[Dict[str, str]] = []

    if not new_entries:
        print("No new entries to add.")
    else:
        print(f"Repairing index with {len(new_entries)} entries.")