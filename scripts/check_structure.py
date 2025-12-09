#!/usr/bin/env python3
"""
check_structure.py
Vérifie la structure critique du projet ITCAA IA :
- Présence des __init__.py
- Présence des fichiers critiques
- Importabilité des modules essentiels
"""

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
    "itcaa_ai_offline.schemas",
    "itcaa_ai_offline.utils",
    "itcaa_ai_offline.predictor",
    "itcaa_ai_offline.index_builder",
    "itcaa_ai_offline.routers",
]

REQUIRED_FILES = [
    SRC / "itcaa_ai_offline" / "config.py",
    SRC / "itcaa_ai_offline" / "model_loader.py",
    SRC / "itcaa_ai_offline" / "schemas.py",
    SRC / "itcaa_ai_offline" / "utils.py",
    SRC / "itcaa_ai_offline" / "predictor.py",
    SRC / "itcaa_ai_offline" / "routers.py",
    SRC / "itcaa_ai_offline" / "index_builder.py",
]

def check_init_files() -> bool:
    print("🔍 Vérification des fichiers __init__.py…")
    ok = True
    for path in REQUIRED_INIT_FILES:
        if not path.exists():
            print(f"❌ Manquant : {path}")
            ok = False
        else:
            print(f"✅ Présent : {path}")
    return ok

def check_required_files() -> bool:
    print("📁 Vérification des fichiers critiques…")
    ok = True
    for path in REQUIRED_FILES:
        if not path.exists():
            print(f"❌ Fichier manquant : {path}")
            ok = False
        else:
            print(f"✅ Présent : {path}")
    return ok

def check_imports() -> bool:
    print("📦 Vérification des imports Python…")
    sys.path.insert(0, str(SRC))
    ok = True
    for module in REQUIRED_MODULES:
        try:
            importlib.import_module(module)
            print(f"✅ Import OK : {module}")
        except Exception as e:
            print(f"❌ Échec import {module} → {e}")
            ok = False
    return ok

def main():
    print("🧠 Vérification structure ITCAA IA en cours…\n")
    ok = check_init_files() and check_required_files() and check_imports()
    if ok:
        print("\n🎯 Structure valide. Prêt pour exécution CI/CD.")
        sys.exit(0)
    else:
        print("\n🚫 Structure invalide. Corrige avant de lancer les tests.")
        sys.exit(1)

if __name__ == "__main__":
    main()