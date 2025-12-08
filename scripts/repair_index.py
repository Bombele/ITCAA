#!/usr/bin/env python3
"""
repair_index.py
Vérifie et répare l'index FAISS utilisé par ITCAA avec embeddings Sentence-Transformers.
Mode incrémental : ajoute uniquement les nouvelles entrées du corpus.
"""

import os
import sys
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# 📂 Définir les chemins robustes
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORPUS_DIR = os.path.join(ROOT_DIR, "src", "itcaa_ai_offline", "data", "corpus")
INDEX_DIR = os.path.join(ROOT_DIR, "src", "itcaa_ai_offline", "data", "index")
INDEX_FILE = os.path.join(INDEX_DIR, "faiss.index")
META_FILE = os.path.join(INDEX_DIR, "index_meta.txt")

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

def load_meta() -> set[str]:
    """Charge les entrées déjà indexées (métadonnées)."""
    if not os.path.isfile(META_FILE):
        return set()
    with open(META_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_meta(texts: list[str]):
    """Sauvegarde les textes indexés dans le fichier meta."""
    os.makedirs(INDEX_DIR, exist_ok=True)
    with open(META_FILE, "w", encoding="utf-8") as f:
        for t in texts:
            f.write(t + "\n")

def build_embeddings(texts: list[str]) -> np.ndarray:
    """Construit les embeddings avec Sentence-Transformers."""
    try:
        model = SentenceTransformer(MODEL_NAME)
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        return embeddings.astype("float32")
    except Exception as e:
        log(f"❌ Erreur lors de la génération des embeddings : {e}")
        sys.exit(1)

def rebuild_index(texts: list[str]):
    """Reconstruit l’index FAISS complet."""
    log("⚠️ Reconstruction complète de l’index FAISS...")
    embeddings = build_embeddings(texts)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_FILE)
    save_meta(texts)
    log(f"✅ Index reconstruit avec {index.ntotal} vecteurs.")

def update_index():
    """Met à jour l’index FAISS en ajoutant uniquement les nouvelles entrées."""
    texts = load_corpus()
    if not texts:
        log("❌ Corpus vide, rien à indexer.")
        sys.exit(1)

    indexed_texts = load_meta()
    new_texts = [t for t in texts if t not in indexed_texts]

    if not index_exists():
        log("⚠️ Index absent, reconstruction complète nécessaire.")
        rebuild_index(texts)
        return

    try:
        index = faiss.read_index(INDEX_FILE)
        log(f"✅ Index FAISS chargé avec {index.ntotal} vecteurs.")
    except Exception as e:
        log(f"❌ Erreur lors du chargement de l’index : {e}")
        rebuild_index(texts)
        return

    if new_texts:
        log(f"📚 {len(new_texts)} nouvelles entrées détectées, ajout à l’index...")
        embeddings = build_embeddings(new_texts)
        if embeddings.shape[1] != index.d:
            log("❌ Dimension des embeddings incompatible avec l’index, reconstruction complète nécessaire.")
            rebuild_index(texts)
            return
        index.add(embeddings)
        faiss.write_index(index, INDEX_FILE)
        save_meta(texts)
        log(f"✅ Index mis à jour avec {index.ntotal} vecteurs.")
    else:
        log("ℹ️ Aucun nouveau texte à indexer. Index inchangé.")

if __name__ == "__main__":
    log("Démarrage de la vérification incrémentale de l’index FAISS...")
    if corpus_exists():
        update_index()
    else:
        log("❌ Aucun corpus trouvé.")
        sys.exit(1)
    log("Fin de la vérification incrémentale.")