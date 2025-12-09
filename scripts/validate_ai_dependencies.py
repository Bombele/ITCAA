"""
Script critique : validate_ai_dependencies.py
Objectif : Vérifier la présence des dépendances IA essentielles (torch, transformers, sentence-transformers, faiss).
Institutionnalisation : audit obligatoire avant exécution des scripts critiques (repair_index, index_builder).
"""

import sys

DEPENDENCIES = [
    ("torch", "PyTorch"),
    ("transformers", "HuggingFace Transformers"),
    ("sentence_transformers", "Sentence-Transformers"),
    ("faiss", "FAISS"),
    ("scikit_learn", "Scikit-Learn"),
]

def main():
    print("🔍 Audit des dépendances IA...")
    missing = []
    for module, name in DEPENDENCIES:
        try:
            __import__(module)
            print(f"✅ {name} disponible ({module})")
        except ImportError:
            print(f"❌ {name} manquant ({module})")
            missing.append(name)

    if missing:
        print("\n❌ Échec audit IA : dépendances manquantes →", ", ".join(missing))
        sys.exit(1)
    else:
        print("\n✅ Audit IA réussi : toutes les dépendances critiques sont présentes.")

if __name__ == "__main__":
    main()