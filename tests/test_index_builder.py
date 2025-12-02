from pathlib import Path
from src.itcaa_ai_offline.data.corpus.index_builder import build_index
from src.itcaa_ai_offline.data.config import PATHS

def test_index_builder_creates_files():
    # Exécute la construction de l'index
    build_index()

    # Vérifie que les fichiers nécessaires ont été générés
    assert PATHS.faiss_index.exists(), "Index FAISS non généré"
    assert PATHS.meta_json.exists(), "Fichier meta.json non généré"

    # Vérifie que les fichiers ne sont pas vides
    assert PATHS.faiss_index.stat().st_size > 0, "Index FAISS vide"
    assert PATHS.meta_json.stat().st_size > 0, "Fichier meta.json vide"