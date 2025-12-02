import os
import importlib
from src.itcaa_ai_offline import config

def test_directories_exist():
    # Vérifie que les dossiers nécessaires existent
    assert config.PATHS.corpus_dir.exists(), "Le dossier corpus n'existe pas"
    assert config.PATHS.index_dir.exists(), "Le dossier index n'existe pas"

def test_default_parameters():
    # Vérifie les valeurs par défaut
    assert config.EMBEDDING_MODEL == "sentence-transformers/all-MiniLM-L6-v2"
    assert config.TOP_K == 3

def test_env_override(monkeypatch):
    # Simule des variables d'environnement
    monkeypatch.setenv("ITCAA_EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    monkeypatch.setenv("ITCAA_TOP_K", "5")

    # Recharger le module pour appliquer les nouvelles valeurs
    import src.itcaa_ai_offline.config as cfg
    importlib.reload(cfg)

    assert cfg.EMBEDDING_MODEL == "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    assert cfg.TOP_K == 5