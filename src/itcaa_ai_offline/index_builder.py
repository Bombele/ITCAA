from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import List, Tuple
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from .config import PATHS, EMBEDDING_MODEL

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def read_corpus_files(corpus_dir: Path) -> List[Tuple[str, str]]:
    docs: List[Tuple[str, str]] = []
    for p in sorted(corpus_dir.glob("*.txt")):
        text = p.read_text(encoding="utf-8").strip()
        if text:
            docs.append((p.name, text))
    if not docs:
        raise FileNotFoundError(f"Aucun document trouvé dans {corpus_dir}")
    logging.info(f"{len(docs)} documents chargés depuis {corpus_dir}")
    return docs

def build_embeddings(texts: List[str]) -> np.ndarray:
    try:
        model = SentenceTransformer(EMBEDDING_MODEL)
        vectors = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        logging.info(f"{len(texts)} embeddings générés avec {EMBEDDING_MODEL}")
        return vectors.astype("float32")
    except Exception as e:
        logging.error(f"Erreur lors de la génération des embeddings: {e}")
        raise

def save_faiss_index(vectors: np.ndarray, meta: List[dict], index_path: Path, meta_path: Path) -> None:
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)  # Inner Product avec vecteurs normalisés = cosinus
    index.add(vectors)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(index_path))
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    logging.info(f"Index FAISS sauvegardé: {index_path}")
    logging.info(f"Métadonnées sauvegardées: {meta_path}")

def build_index(incremental: bool = False) -> None:
    docs = read_corpus_files(PATHS.corpus_dir)
    texts = [t for _, t in docs]
    vectors = build_embeddings(texts)
    meta = [{"id": i, "filename": fname, "text": text} for i, (fname, text) in enumerate(docs)]
    save_faiss_index(vectors, meta, PATHS.faiss_index, PATHS.meta_json)

if __name__ == "__main__":
    try:
        build_index()
        logging.info(f"✅ Index construit: {PATHS.faiss_index}")
    except Exception as e:
        logging.error(f"❌ Échec de la construction de l'index: {e}")
