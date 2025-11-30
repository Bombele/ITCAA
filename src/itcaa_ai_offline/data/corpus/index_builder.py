import json
import logging
from pathlib import Path
from typing import List, Dict

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from src.itcaa_ai_offline.data.config import PATHS, EMBEDDING_MODEL

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def build_index(incremental: bool = False) -> None:
    """
    Construit ou met à jour un index FAISS à partir des fichiers texte dans corpus/.
    - Si incremental=False : reconstruit l'index complet.
    - Si incremental=True : ajoute uniquement les nouveaux passages non présents dans meta.json.
    """

    model = SentenceTransformer(EMBEDDING_MODEL)

    texts: List[str] = []
    meta: List[Dict] = []

    # Charger les métadonnées existantes si mode incrémental
    if incremental and PATHS.meta_json.exists():
        existing_meta = json.loads(PATHS.meta_json.read_text(encoding="utf-8"))
        existing_ids = {m["filename"] + str(m["paragraph"]) for m in existing_meta}
        meta = existing_meta
        logging.info(f"Mode incrémental : {len(existing_meta)} passages déjà indexés.")
    else:
        existing_ids = set()

    # Lire tous les fichiers du corpus
    corpus_files = sorted(PATHS.corpus_dir.glob("*.txt"))
    if not corpus_files:
        raise FileNotFoundError(f"Aucun fichier trouvé dans {PATHS.corpus_dir}")

    new_entries = []
    for file in corpus_files:
        try:
            content = file.read_text(encoding="utf-8").strip().split("\n")
        except Exception as e:
            logging.error(f"Erreur lecture fichier {file}: {e}")
            continue

        for j, paragraph in enumerate(content):
            if paragraph.strip():
                unique_id = file.name + str(j)
                if unique_id not in existing_ids:
                    texts.append(paragraph.strip())
                    new_entries.append({
                        "id": len(meta) + len(new_entries),
                        "filename": file.name,
                        "paragraph": j,
                        "text": paragraph.strip()
                    })

    if not texts and not meta:
        raise ValueError("Corpus vide: aucun paragraphe valide trouvé.")

    # Générer les embeddings uniquement pour les nouveaux passages
    if texts:
        logging.info(f"Génération des embeddings pour {len(texts)} nouveaux passages...")
        vectors = model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        # Charger ou créer l'index FAISS
        if incremental and PATHS.faiss_index.exists():
            index = faiss.read_index(str(PATHS.faiss_index))
        else:
            dim = vectors.shape[1]
            index = faiss.IndexFlatIP(dim)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--incremental", action="store_true", help="Mettre à jour l'index incrémentalement")
    args = parser.parse_args()

    build_index(incremental=args.incremental)
