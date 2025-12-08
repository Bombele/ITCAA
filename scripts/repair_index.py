#!/usr/bin/env python3
"""
repair_index.py
Vérifie et répare l'index FAISS utilisé par ITCAA.
"""

import os
import sys
import faiss
import numpy as np

# 📂 Définir les chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(BASE_DIR, "..", "src", "itcaa_ai_offline", "data", "corpus")
INDEX_DIR = os.path.join(BASE_DIR, "..", "src", "itcaa_ai_offline", "data", "index")
INDEX_FILE = os.path.join(INDEX_DIR, "faiss.index")

def log(msg: str):
    print(f"🔍 [repair-index] {msg}", flush=True)

def corpus_exists() -> bool:
    return os.path.isdir(CORPUS_DIR) and any(f.endswith(".txt") for f in os.listdir(CORPUS_DIR))

def index_exists() -> bool:
    return os.path.isfile(INDEX_FILE)

def rebuild_index():
    """Reconstruit un index FAISS minimal à partir du corpus."""
    log("Reconstruction de l’index FAISS...")
    if not corpus_exists():
        log("❌ Aucun corpus trouvé, impossible de reconstruire l’index.")
        sys.exit(1)

    # Exemple minimal : vecteurs aléatoires pour placeholder
    # ⚠️ À remplacer par ton vrai embedding (transformers/sentence-transformers)
    dim = 128
    vectors = np.random.rand(10, dim).astype("float32")

    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_FILE)
    log(f"✅ Index reconstruit et sauvegardé dans {INDEX_FILE}")

def verify_index():
    """Vérifie si l’index FAISS est lisible, sinon le reconstruit."""
    if not index_exists():
        log("⚠️ Index FAISS absent, reconstruction nécessaire.")
        rebuild_index()
        return

    try:
        index = faiss.read_index(INDEX_FILE)
        log(f"✅ Index FAISS chargé avec {index.ntotal} vecteurs.")
    except Exception as e:
        log(f"❌ Erreur lors du chargement de l’index : {e}")
        rebuild_index()

if __name__ == "__main__":
    log("Démarrage de la vérification de l’index FAISS...")
    verify_index()
    log("Fin de la vérification.")