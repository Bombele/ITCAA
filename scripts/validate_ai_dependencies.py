#!/usr/bin/env python3
"""
validate_ai_dependencies.py
Audit des dépendances IA critiques pour ITCAA.
Ce script vérifie la présence des librairies nécessaires avant exécution des scripts IA.
"""

import sys

# Liste des dépendances critiques à vérifier
DEPENDENCIES = [
    "torch",
    "transformers",
    "sentence_transformers",
    "faiss",
    "scikit_learn"
]

def main():
    missing = []
    for dep in DEPENDENCIES:
        try:
            __import__(dep)
            print(f"✅ {dep} disponible")
        except ImportError:
            print(f"❌ {dep} manquant")
            missing.append(dep)

    if missing:
        print("\n❌ Audit IA échoué : dépendances manquantes ->", ", ".join(missing))
        sys.exit(1)
    else:
        print("\n✅ Audit IA réussi : toutes les dépendances sont présentes")

if __name__ == "__main__":
    main()