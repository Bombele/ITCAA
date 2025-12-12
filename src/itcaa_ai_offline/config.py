from pathlib import Path
from dataclasses import dataclass
import os

# Définir la racine du projet (2 niveaux au-dessus de ce fichier)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CORPUS_DIR = DATA_DIR / "corpus"
INDEX_DIR = DATA_DIR / "index"

# Création automatique des dossiers si manquants
for directory in [DATA_DIR, CORPUS_DIR, INDEX_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

@dataclass(frozen=True)
class Paths:
    corpus_dir: Path = CORPUS_DIR
    index_dir: Path = INDEX_DIR
    faiss_index: Path = INDEX_DIR / "faiss.index"
    meta_json: Path = INDEX_DIR / "meta.json"

PATHS = Paths()

# Paramètres configurables via variables d'environnement
EMBEDDING_MODEL = os.getenv(
    "ITCAA_EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"  # valeur par défaut
)

TOP_K = int(os.getenv("ITCAA_TOP_K", "3"))

# src/itcaa_ai_offline/config.py
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict

# Paramètres globaux
SETTINGS: Dict[str, Any] = {
    "corpus_path": Path("data/corpus"),
    "index_path": Path("build/index.faiss"),
    "model_path": Path("models/offline_model"),
    "log_level": "INFO",
}