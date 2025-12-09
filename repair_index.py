#!/usr/bin/env python3
"""
repair_index.py
Vérifie la cohérence entre meta.json et faiss.index.
Institutionnalisation pour CI/CD ITCAA : logs explicites et robustesse.
"""

import json
import logging
import sys
import faiss
from pathlib import Path
from src.itcaa_ai_offline.data.config import PATHS
from src.itcaa_ai_offline.data.corpus.index_builder import build_index

# Configuration des logs institutionnels
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [repair-index] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def check_and_repair_index() -> bool:
    """
    Vérifie la cohérence entre meta.json et faiss.index.
    Si incohérence détectée ou erreur, reconstruit l'index complet.
    Retourne True si l'index est cohérent ou reconstruit avec succès, False sinon.
    """
    try:
        # Vérifier existence des fichiers
        if not PATHS.faiss_index.exists() or not PATHS.meta_json.exists():
            logging.warning("❌ Index FAISS ou meta.json manquant → reconstruction complète.")
            build_index(incremental=False)
            logging.info("✅ Reconstruction effectuée (absence de fichiers).")
            return True

        # Charger index FAISS
        try:
            index = faiss.read_index(str(PATHS.faiss_index))
            logging.info(f"📂 Index FAISS chargé avec {index.ntotal} vecteurs.")
        except Exception as e:
            logging.error(f"❌ Impossible de lire l'index FAISS : {e}")
            logging.info("🔄 Reconstruction complète de l'index...")
            build_index(incremental=False)
            return False

        # Charger métadonnées
        try:
            meta_text = PATHS.meta_json.read_text(encoding="utf-8")
            meta = json.loads(meta_text)
            logging.info(f"📂 meta.json chargé avec {len(meta)} entrées.")
        except json.JSONDecodeError as e:
            logging.error(f"❌ meta.json corrompu : {e}")
            logging.info("🔄 Reconstruction complète de l'index...")
            build_index(incremental=False)
            return False
        except Exception as e:
            logging.error(f"❌ Erreur inattendue lors de la lecture de meta.json : {e}")
            logging.info("🔄 Reconstruction complète de l'index...")
            build_index(incremental=False)
            return False

        # Vérifier cohérence
        if not isinstance(meta, list):
            logging.error("❌ meta.json n'est pas une liste valide → reconstruction.")
            build_index(incremental=False)
            return False

        if len(meta) != index.ntotal:
            logging.error(
                f"❌ Incohérence détectée : meta.json={len(meta)} vs FAISS={index.ntotal}. "
                "→ Reconstruction complète en cours..."
            )
            build_index(incremental=False)
            return False

        logging.info("✅ Index FAISS et meta.json sont cohérents.")
        return True

    except Exception as e:
        logging.exception(f"❌ Erreur inattendue lors de la vérification : {e}")
        logging.info("🔄 Reconstruction forcée de l'index...")
        build_index(incremental=False)
        return False


if __name__ == "__main__":
    success = check_and_repair_index()
    if success:
        logging.info("🎯 Processus de vérification terminé avec succès.")
        sys.exit(0)
    else:
        logging.warning("🚫 Processus terminé avec incohérences corrigées.")
        sys.exit(1)