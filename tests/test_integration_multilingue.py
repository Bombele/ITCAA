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


def test_multilingue_index_builder():
    # Créer un corpus multilingue avec les 6 langues ONU
    corpus_file = config.PATHS.corpus_dir / "test_multilingue.txt"
    corpus_file.write_text(
        "Bonjour ITCAA.\n"      # Français
        "Hello ITCAA.\n"        # Anglais
        "Hola ITCAA.\n"         # Espagnol
        "مرحبا ITCAA.\n"        # Arabe
        "你好 ITCAA。\n"          # Chinois
        "Привет ITCAA.\n",      # Russe
        encoding="utf-8"
    )

    # Reconstruire l'index complet
    build_index(incremental=False)

    # Vérifier que l'index FAISS existe
    assert config.PATHS.faiss_index.exists(), "Index FAISS non généré"

    # Vérifier que meta.json existe
    assert config.PATHS.meta_json.exists(), "meta.json non généré"

    # Charger l'index et les métadonnées
    index = faiss.read_index(str(config.PATHS.faiss_index))
    meta = json.loads(config.PATHS.meta_json.read_text(encoding="utf-8"))

    # Vérifier cohérence
    assert len(meta) == index.ntotal, (
        f"Incohérence : meta.json={len(meta)} vs FAISS={index.ntotal}"
    )
    assert index.ntotal == 6, "L'index FAISS doit contenir 6 vecteurs (une par langue ONU)"