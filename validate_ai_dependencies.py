#!/usr/bin/env python3
"""
✅ Audit IA – Vérifie la présence des dépendances critiques
"""

import sys

DEPENDENCIES = {
    "torch": "torch",
    "transformers": "transformers",
    "sentence-transformers": "sentence_transformers",
    "faiss": "faiss",
    "scikit-learn": "sklearn"
}

missing = []

for name, module in DEPENDENCIES.items():
    try:
        __import__(module)
        print(f"✅ {name} importé avec succès")
    except ImportError:
        print(f"❌ {name} manquant")
        missing.append(name)
    except Exception as e:
        print(f"⚠️ Erreur inattendue lors de l'import de {name} : {e}")
        missing.append(name)

if missing:
    print(f"\n❌ Audit IA échoué : dépendances manquantes → {', '.join(missing)}")
    sys.exit(1)

print("\n✅ Audit IA réussi : toutes les dépendances sont présentes")
sys.exit(0)