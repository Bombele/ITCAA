import json
import faiss
import shutil
import pytest
from pathlib import Path

from src.itcaa_ai_offline import config
from src.itcaa_ai_offline.data.corpus.index_builder import build_index

@pytest.fixture(autouse=True)
def clean_index_dir(tmp_path, monkeypatch):
    """
    Prépare un environnement isolé pour éviter les conflits avec l'index réel.
    Chaque test utilise un répertoire temporaire pour corpus et index.
    """
    # Rediriger les chemins vers un dossier temporaire
    monkeypatch.setattr(config.PATHS, "index_dir", tmp_path / "index")
    monkeypatch.setattr(config.PATHS, "faiss_index", tmp_path / "index/faiss.index")
    monkeypatch.setattr(config.PATHS, "meta_json", tmp_path / "index/meta.json")
    monkeypatch.setattr(config.PATHS, "corpus_dir", tmp_path / "corpus")

    # Créer les dossiers nécessaires
    config.PATHS.index_dir.mkdir(parents=True, exist_ok=True)
    config.PATHS.corpus_dir.mkdir(parents=True, exist_ok=True)

    yield

    # Nettoyage après test
    shutil.rmtree(tmp_path)

def test_integration_index_builder():
    # Créer un corpus minimal
    corpus_file = config.PATHS.corpus_dir / "test_corpus.txt"
    corpus_file.write_text("Bonjour ITCAA.\nHello ITCAA.\nHola ITCAA.", encoding="utf-8")

    # Reconstruire l'index complet
    build_index(incremental=False)

    # Vérifier que l'index FAISS existe
    assert config.PATHS.faiss_index.exists(), "Index FAISS non généré"

    # Vérifier que meta.json existe
    assert config.PATHS.meta_json.exists(), "meta.json non généré"

    # Charger l'index et les métadonnées
    index = faiss.read_index