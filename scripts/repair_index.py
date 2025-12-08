#!/usr/bin/env python3
"""
repair_index.py
Vérifie et répare l'index FAISS utilisé par ITCAA avec embeddings Sentence-Transformers.
"""

import os
import sys
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# 📂 Définir les chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(BASE_DIR, "..", "src", "itcaa_ai_offline", "data", "corpus")
INDEX_DIR = os.path.join(BASE_DIR, "..", "src", "itcaa_ai_offline", "data", "index")
INDEX_FILE = os.path.join(INDEX_DIR, "faiss.index")

# ⚙️ Choisir le modèle d’embedding
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def log(msg: str):
    print(f"🔍 [repair-index] {msg}", flush=True)

def corpus_exists() -> bool:
    return os.path.isdir(CORPUS_DIR) and any(f.endswith(".txt") for f in os.listdir(CORPUS_DIR))

def index_exists() -> bool:
    return os.path.isfile(INDEX_FILE)

def load_corpus() -> list[str]:
    """Charge tous les fichiers texte du corpus."""
    texts = []
    for fname in os.listdir(CORPUS_DIR):
        if fname.endswith(".txt"):
            with open(os.path.join(CORPUS_DIR, fname), "r", encoding="utf-8") as f:
                texts.extend([line.strip() for line in f if line.strip()])
    return texts

def rebuild_index():
    """Reconstruit un index FAISS à partir du corpus avec embeddings Sentence-Transformers."""
    log("Reconstruction de l’index FAISS avec embeddings...")
    if not corpus_exists():
        log("❌ Aucun corpus trouvé, impossible de reconstruire l’index.")
        sys.exit(1)

    texts = load_corpus()
    log(f"📚 Corpus chargé avec {len(texts)} entrées.")

    # Charger le modèle
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype("float32"))

    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_FILE)
    log(f"✅ Index reconstruit et sauvegardé dans {INDEX_FILE} avec {index.ntotal} vecteurs.")

def verify_index():
    """Vérifie si l’index FAISS est lisible, sinon le reconstruit."""
    if not index_exists():
        log("⚠️ Index FAISS absent, reconstruction nécessaire.")
        rebuild_index()
        return

    try:
        index = faiss.read_index(INDEX_FILE)
        log(f"✅ Index FAISS chargé avec {index.ntotal} vecteurs.")
        if index.ntotal == 0:
            log("⚠️ Index vide, reconstruction nécessaire.")
            rebuild_index()
    except Exception as e:
        log(f"❌ Erreur lors du chargement de l’index : {e}")
        rebuild_index()

if __name__ == "__main__":
    log("Démarrage de la vérification de l’index FAISS...")
    verify_index()
    log("Fin de la vérification.")