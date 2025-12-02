import faiss
from src.itcaa_ai_offline.data.config import PATHS

def test_faiss_index_valid():
    # Vérifie que le fichier index existe
    assert PATHS.faiss_index.exists(), "Fichier FAISS index manquant"

    # Charge l'index FAISS
    index = faiss.read_index(str(PATHS.faiss_index))

    # Vérifie qu'il contient au moins un vecteur
    assert index.ntotal > 0, "Index FAISS vide ou corrompu"