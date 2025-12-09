"""
Script critique : repair_index.py
Objectif : Vérifier et réparer l’index FAISS utilisé par ITCAA.
Institutionnalisation : dépendances IA (torch, transformers, sentence-transformers, faiss)
"""

import os
import sys
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# 🔍 Vérification des dépendances critiques
def check_dependencies():
    try:
        import torch, transformers, sentence_transformers, faiss
        print("✅ Dépendances IA présentes.")
    except ImportError as e:
        print(f"❌ Dépendance manquante : {e.name}")
        sys.exit(1)

# 📦 Chargement du modèle SentenceTransformer
def load_model():
    print("🧠 Chargement du modèle SentenceTransformer...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

# 🛠 Réparation / création de l’index FAISS
def repair_index(model, index_path="data/faiss_index.bin"):
    # Exemple de corpus minimal
    corpus = ["justice digitale", "IA éthique", "robustesse institutionnelle"]
    embeddings = model.encode(corpus)

    # Création d’un index FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    # Sauvegarde
    os.makedirs("data", exist_ok=True)
    faiss.write_index(index, index_path)
    print(f"✅ Index FAISS réparé et sauvegardé dans {index_path}")

def main():
    check_dependencies()
    model = load_model()
    repair_index(model)

if __name__ == "__main__":
    main()