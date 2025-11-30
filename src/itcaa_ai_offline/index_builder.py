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
    return docs

def build_embeddings(texts: List[str]) -> np.ndarray:
    model = SentenceTransformer(EMBEDDING_MODEL)
    vectors = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return vectors.astype("float32")

def save_faiss_index(index, meta: List[dict], index_path: Path, meta_path: Path) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(index_path))
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    logging.info(f"Index FAISS sauvegardé: {index_path}")
    logging.info(f"Métadonnées sauvegardées: {meta_path}")

def build_index(incremental: bool = False) -> None:
    docs = read_corpus_files(PATHS.corpus_dir)

    # Charger meta existant si incrémental
    if incremental and PATHS.meta_json.exists() and PATHS.faiss_index.exists():
        meta = json.loads(PATHS.meta_json.read_text(encoding="utf-8"))
        indexed_files = {m["filename"] for m in meta}
        new_docs = [(fname, text) for fname, text in docs if fname not in indexed_files]

        if not new_docs:
            logging.info("Aucun nouveau document à indexer.")
            return

        texts = [t for _, t in new_docs]
        vectors = build_embeddings(texts)

        # Charger l'index existant
        index = faiss.read_index(str(PATHS.faiss_index))

        # Ajouter les nouveaux vecteurs
        index.add(vectors)

        # Mettre à jour meta
        start_id = len(meta)
        for i, (fname, text) in enumerate(new_docs, start=start_id):
            meta.append({"id": i, "filename": fname, "text": text})

        save_faiss_index(index, meta, PATHS.faiss_index, PATHS.meta_json)
        logging.info(f"{len(new_docs)} nouveaux documents ajoutés à l'index.")
    else:
        # Reconstruction complète
        texts = [t for _, t in docs]
        vectors = build_embeddings(texts)
        meta = [{"id": i, "filename": fname, "text": text} for i, (fname, text) in enumerate(docs)]
        dim = vectors.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(vectors)
        save_faiss_index(index, meta, PATHS.faiss_index, PATHS.meta_json)
        logging.info("Index reconstruit entièrement.")

if __name__ == "__main__":
    build_index(incremental=True)
    logging.info(f"✅ Index mis à jour: {PATHS.faiss_index}")
