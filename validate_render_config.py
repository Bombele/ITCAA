#!/usr/bin/env python3
import os
import sys
import yaml
import logging

# 📂 Configuration des logs
logging.basicConfig(
    filename="logs/validate_render_config.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

EXPECTED_START_CMD = "PYTHONPATH=src python -m uvicorn apps.api.main:app --host 0.0.0.0 --port $PORT"
REQUIRED_KEYS = ["startCommand", "services"]

def check_file(path: str) -> bool:
    if os.path.isfile(path):
        print(f"✅ Fichier {path} trouvé")
        logging.info("Fichier %s trouvé", path)
        return True
    else:
        print(f"❌ Fichier {path} manquant")
        logging.error("Fichier %s manquant", path)
        print(f"➡️ Suggestion : créer ou restaurer {path}")
        return False

def check_folder(path: str) -> bool:
    if os.path.isdir(path):
        print(f"✅ Dossier {path}/ trouvé")
        logging.info("Dossier %s trouvé", path)
        return True
    else:
        print(f"❌ Dossier {path}/ manquant")
        logging.error("Dossier %s manquant", path)
        print(f"➡️ Suggestion : créer le dossier {path}/")
        return False

def check_render_yaml() -> bool:
    path = "render.yaml"
    if not check_file(path):
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        print(f"❌ Erreur YAML dans {path}: {e}")
        logging.error("Erreur YAML dans %s: %s", path, e)
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {path}: {e}")
        logging.error("Erreur lecture %s: %s", path, e)
        return False

    # Vérification des clés obligatoires
    missing_keys = [k for k in REQUIRED_KEYS if k not in data]
    if missing_keys:
        print(f"❌ Clés manquantes dans render.yaml: {missing_keys}")
        logging.error("Clés manquantes: %s", missing_keys)
        return False

    # Vérification du startCommand
    start_cmd = data.get("startCommand", "").strip()
    if start_cmd == EXPECTED_START_CMD:
        print("✅ startCommand correct dans render.yaml")
        logging.info("startCommand correct")
    else:
        print("❌ startCommand incorrect dans render.yaml")
        print(f"➡️ Actuel : {start_cmd}")
        print(f"➡️ Attendu : {EXPECTED_START_CMD}")
        logging.error("startCommand incorrect: %s", start_cmd)
        return False

    return True

def main():
    print("🔍 Validation de la configuration Render")
    logging.info("Début validation configuration Render")

    ok_yaml = check_render_yaml()
    ok_folder = check_folder("src")

    if ok_yaml and ok_folder:
        print("✅ Configuration Render valide")
        logging.info("Configuration Render valide")
        sys.exit(0)
    else:
        print("❌ Configuration Render invalide")
        logging.error("Configuration Render invalide")
        sys.exit(1)

if __name__ == "__main__":
    main()
