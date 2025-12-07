#!/usr/bin/env python3
import subprocess
import sys
import logging
from typing import List

# 📂 Configuration des logs
logging.basicConfig(
    filename="logs/validate_dependencies.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def run_command(cmd: List[str]) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logging.info("Commande exécutée avec succès: %s", " ".join(cmd))
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error("Erreur lors de l'exécution de %s: %s", cmd, e.stderr)
        print(f"❌ Erreur lors de l'exécution de {cmd}: {e.stderr}")
        sys.exit(1)

def main():
    print("🔍 Vérification des dépendances Python...")
    logging.info("Début de la validation des dépendances")

    # Étape 1 : pip check
    print("\n=== Étape 1 : pip check ===")
    pip_check_output = run_command([sys.executable, "-m", "pip", "check"])
    if pip_check_output.strip():
        print(pip_check_output)
        logging.warning("pip check a détecté des incohérences:\n%s", pip_check_output)
    else:
        print("✅ Aucune incohérence détectée avec pip check.")
        logging.info("pip check : aucune incohérence détectée")

    # Étape 2 : pipdeptree
    print("\n=== Étape 2 : pipdeptree ===")
    try:
        __import__("pipdeptree")
        pipdeptree_output = run_command([sys.executable, "-m", "pipdeptree"])
        print(pipdeptree_output)
        logging.info("pipdeptree exécuté avec succès")
    except ImportError:
        print("⚠️ pipdeptree non installé. Installez-le avec `pip install pipdeptree`.")
        logging.warning("pipdeptree non installé")

    print("\n✅ Validation des dépendances terminée.")
    logging.info("Validation des dépendances terminée avec succès")

if __name__ == "__main__":
    main()
