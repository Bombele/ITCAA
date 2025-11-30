# tests/test_index_builder.py
from pathlib import Path
from src.itcaa_ai_offline.data.corpus.index_builder import build_index
from src.itcaa_ai_offline.data.config import PATHS

def test_index_builder_creates_files():
    build_index()
    assert PATHS.faiss_index.exists(), "Index FAISS non généré"
    assert PATHS.meta_json.exists(), "Fichier meta.json non généré"