import json
import faiss
from pathlib import Path
import shutil
import pytest

from src.itcaa_ai_offline import config
from src.itcaa_ai_offline.data.corpus.index_builder import build_index

@pytest.fixture(autouse=True)
def clean_index_dir(tmp_path, monkeypatch):
    """
    Prépare un environnement isolé pour éviter les conflits avec l'index réel.
    """
    monkeypatch.setattr(config.PATHS, "index_dir", tmp_path / "index")
    monkeypatch.setattr(config.PATHS, "faiss_index", tmp_path / "index/faiss.index")
    monkeypatch.setattr(config.PATHS, "meta_json", tmp_path / "index/meta.json")
    monkeypatch.setattr(config.PATHS, "corpus_dir", tmp_path / "corpus")

    config.PATHS.index_dir.mkdir(parents=True, exist_ok=True)
    config.PATHS.corpus_dir.mkdir(parents=True, exist_ok=True)

    yield
    shutil.rmtree(tmp_path)


def test_incremental_index_builder():
    # Étape 1 : créer un corpus initial
    corpus_file1 = config.PATHS.corpus_dir / "doc1.txt"
    corpus_file1.write_text("Bonjour ITCAA.", encoding="utf-8")

    build_index(incremental=False)

    # Charger index et meta
    index1 = faiss.read_index(str(config.PATHS.faiss_index))
    meta1 = json.loads(config.PATHS.meta_json.read_text(encoding="utf-8"))

    assert index1.ntotal == 1
    assert len(meta1) == 1

    # Étape 2 : ajouter un nouveau fichier corpus
    corpus_file2 = config.PATHS.corpus_dir / "doc2.txt"
    corpus_file2.write_text("Hello ITCAA.", encoding="utf-8")

    build_index(incremental=True)

    # Charger index et meta après incrément
    index2 = faiss.read_index(str(config.PATHS.faiss_index))
    meta2 = json.loads(config.PATHS.meta_json.read_text(encoding="utf-8"))

    # Vérifier que l'index contient maintenant 2 vecteurs
    assert index2.ntotal == 2, "Index FAISS doit contenir 2 vecteurs après ajout incrémental"
    assert len(meta2) == 2, "meta.json doit contenir 2 entrées après ajout incrémental"

    # Vérifier que les deux fichiers sont bien présents dans meta.json
    filenames = {m["filename"] for m in meta2}
    assert "doc1.txt" in filenames
    assert "doc2.txt" in filenames