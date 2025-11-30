import json
import faiss
from src.itcaa_ai_offline.data.config import PATHS

def test_faiss_meta_coherence():
    # Vérifie que les fichiers existent
    assert PATHS.faiss_index.exists(), "Fichier FAISS index manquant"
    assert PATHS.meta_json.exists(), "Fichier meta.json manquant"

    # Charger l'index FAISS
    index = faiss.read_index(str(PATHS.faiss_index))

    # Charger les métadonnées
    meta = json.loads(PATHS.meta_json.read_text(encoding="utf-8"))

    # Vérifier la cohérence
    assert len(meta) == index.ntotal, (
        f"Incohérence : meta.json contient {len(meta)} passages "
        f"mais l'index FAISS contient {index.ntotal} vecteurs."
    )