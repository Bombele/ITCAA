import os
import sys
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
TESTS = ROOT / "tests"

REQUIRED_INIT_FILES = [
    SRC / "__init__.py",
    SRC / "itcaa_ai_offline" / "__init__.py",
    TESTS / "__init__.py",
]

REQUIRED_MODULES = [
    "src.itcaa_ai_offline.schemas",
    "src.itcaa_ai_offline.utils",
    "src.itcaa_ai_offline.predictor",
    "src.itcaa_ai_offline.index_builder",
]

REQUIRED_FILES = [
    SRC / "itcaa_ai_offline" / "config.py",
    SRC / "itcaa_ai_offline" / "model_loader.py",
    SRC / "itcaa_ai_offline" / "schemas.py",
    SRC / "itcaa_ai_offline" / "utils.py",
]

def check_init_files():
    print("🔍 Vérification des fichiers __init__.py…")
    for path in REQUIRED_INIT_FILES:
        if not path.exists():
            print(f"❌ Manquant : {path}")
            return False
    print("✅ Tous les fichiers __init__.py sont présents.")
    return True

def check_required_files():
    print("📁 Vérification des fichiers critiques…")
    for path in REQUIRED_FILES:
        if not path.exists():
            print(f"❌ Fichier manquant : {path}")
            return False
    print("✅ Tous les fichiers critiques sont présents.")
    return True

def check_imports():
    print("📦 Vérification des imports Python…")
    sys.path.insert(0, str(SRC))
    for module in REQUIRED_MODULES:
        try:
            importlib.import_module(module)
            print(f"✅ Import OK : {module}")
        except Exception as e:
            print(f"❌ Échec import {module} → {e}")
            return False
    return True

def main():
    print("🧠 Vérification structure ITCAA IA en cours…\n")
    ok = (
        check_init_files()
        and check_required_files()
        and check_imports()
    )
    if ok:
        print("\n🎯 Structure valide. Prêt pour exécution CI/CD.")
        sys.exit(0)
    else:
        print("\n🚫 Structure invalide. Corrige avant de lancer les tests.")
        sys.exit(1)

if __name__ == "__main__":
    main()