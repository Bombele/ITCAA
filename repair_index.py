import json
import logging
import faiss
from src.itcaa_ai_offline.data.config import PATHS
from src.itcaa_ai_offline.data.corpus.index_builder import build_index

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def check_and_repair_index():
    """
    Vérifie la cohérence entre meta.json et faiss.index.
    Si incohérence détectée, reconstruit l'index complet.
    """
    try:
        # Vérifier existence des fichiers
        if not PATHS.faiss_index.exists() or not PATHS.meta_json.exists():
            logging.warning("Index ou meta.json manquant → reconstruction complète.")
            build_index(incremental=False)
            return

        # Charger index et métadonnées
        index = faiss.read_index(str(PATHS.faiss_index))
        meta = json.loads(PATHS.meta_json.read_text(encoding="utf-8"))

        # Vérifier cohérence
        if len(meta) != index.ntotal:
            logging.error(
                f"Incohérence détectée : meta.json={len(meta)} vs FAISS={index.ntotal}. "
                "Reconstruction complète en cours..."
            )
            build_index(incremental=False)
        else:
            logging.info("✅ Index FAISS et meta.json sont cohérents.")
    except Exception as e:
        logging.error(f"Erreur lors de la vérification : {e}")
        logging.info("Reconstruction forcée de l'index...")
        build_index(incremental=False)


if __name__ == "__main__":
    check_and_repair_index()