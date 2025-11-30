import json
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from .config import PATHS, EMBEDDING_MODEL


def build_index() -> None:
    """
    Construit un index FAISS à partir des fichiers texte dans corpus/.
    Chaque paragraphe est transformé en vecteur avec SentenceTransformer.
    Les métadonnées sont sauvegardées dans meta.json.
    """

    # Charger le modèle d'embedding
    model = SentenceTransformer(EMBEDDING_MODEL)

    texts: list[str] = []
    meta: list[dict] = []

    # Lire tous les fichiers du corpus
    corpus_files = sorted(PATHS.corpus_dir.glob("*.txt"))
    if not corpus_files:
        raise FileNotFoundError(f"Aucun fichier trouvé dans {PATHS.corpus_dir}")

    for file in corpus_files:
        try:
            content = file.read_text(encoding="utf-8").strip().split("\n")
        except Exception as e:
            raise RuntimeError(f"Erreur lecture fichier {file}: {e}")

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

    print(f"✅ Index reconstruit avec {len(meta)} passages provenant de {len(corpus_files)} fichiers.")


if __name__ == "__main__":
    build_index()
