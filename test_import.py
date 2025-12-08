#!/usr/bin/env python3
import sys
import pathlib
import importlib
import logging

# 📂 Configuration des logs
logging.basicConfig(
    filename="logs/test_import.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# 📂 Ajout du chemin src au PYTHONPATH
SRC_PATH = pathlib.Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SRC_PATH))

try:
    module = importlib.import_module("apps.api.main")
    if hasattr(module, "app"):
        print("✅ Import réussi : app détecté")
        logging.info("Import réussi : apps.api.main avec app")
    else:
        print("⚠️ Import réussi mais 'app' non trouvé")
        logging.warning("Import réussi mais 'app' non trouvé dans apps.api.main")
except Exception as e:
    print(f"❌ Échec de l'import : {e}")
    logging.error(f"Échec de l'import : {e}")
    sys.exit(1)

try:
    from src.apps.api.main import app
    print("✅ Import API réussi")
except Exception as e:
    print("❌ Échec d'import API :", e)
    exit(1)