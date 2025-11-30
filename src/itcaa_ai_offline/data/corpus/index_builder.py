import json
import logging
from pathlib import Path
from typing import List, Dict

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Import absolu recommandé pour éviter les erreurs d'exécution directe
from src.itcaa_ai_offline.data.config import PATHS, EMBEDDING_MODEL

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def build_index() -> None:
    """
    Construit un index FAISS à partir des fichiers texte dans corpus/.
    Chaque paragraphe est transformé en vecteur avec SentenceTransformer.
    Les métadonnées sont sauvegardées dans meta.json.
    """

    # Charger le modèle d'embedding
    logging.info(f"Chargement du modèle d'embedding : {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    texts: List[str] = []
    meta: List[Dict] = []

    # Lire tous les fichiers du corpus
    corpus_files = sorted(PATHS.corpus_dir.glob("*.txt"))
    if not corpus_files:
        raise FileNotFoundError(f"Aucun fichier trouvé dans {PATHS.corpus_dir}")

    for file in corpus_files:
        try:
            content = file.read_text(encoding="utf-8").strip().split("\n")
        except Exception as e:
            logging.error(f"Erreur lecture fichier {file}: {e}")
            continue  # on ignore le fichier corrompu au lieu de bloquer tout

        for j, paragraph in enumerate(content):
            if paragraph.strip():
                texts.append(paragraph.strip())
                meta.append({
                    "id": len(meta),
                    "filename": file.name,
                    "paragraph": j,
                    "text": paragraph.strip()
                })

    if not texts:
        raise ValueError("Corpus vide: aucun paragraphe valide trouvé.")

    # Générer les embeddings
    logging.info(f"Génération des embeddings pour {len(texts)} passages...")
    vectors = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    # Construire l'index FAISS
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)  # Inner Product (cosinus avec vecteurs normalisés)
    index.add(vectors)

    # Sauvegarder l'index et les métadonnées
    PATHS.index_dir.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(PATHS.faiss_index))
    PATHS.meta_json.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    logging.info(f"✅ Index reconstruit avec {len(meta)} passages provenant de {len
