# src/itcaa_ai_offline/utils.py
import logging
import datetime
import os
from typing import List, Union

# 📌 Assurer l’existence du dossier logs
LOG_DIR = "logs"
try:
    os.makedirs(LOG_DIR, exist_ok=True)
except Exception as e:
    print(f"⚠️ Impossible de créer le dossier logs : {e}")
    LOG_DIR = None  # fallback vers console uniquement

# 📌 Configuration du logger (éviter double config)
logger = logging.getLogger("ITCAA_AI_Offline")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # Fichier log si possible
    if LOG_DIR:
        try:
            file_handler = logging.FileHandler(os.path.join(LOG_DIR, "ai_offline.log"), encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"⚠️ Impossible d’écrire dans le fichier log : {e}")

    # Console log
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


# 🧹 Prétraitement des données
def normalize_features(features: List[Union[float, str]]) -> List[float]:
    """
    Normalise une liste de valeurs numériques entre 0 et 1.
    Ignore les valeurs non numériques (texte).
    """
    numeric_features = [float(f) for f in features if isinstance(f, (int, float))]
    if not numeric_features:
        raise ValueError("La liste des features ne contient aucune valeur numérique.")

    min_val, max_val = min(numeric_features), max(numeric_features)
    if min_val == max_val:
        return [0.0 for _ in numeric_features]

    return [(f - min_val) / (max_val - min_val) for f in numeric_features]


# 📝 Auditabilité : journalisation des prédictions
def log_prediction(input_data: List[Union[float, str]], label: Union[int, str], confidence: float) -> str:
    """
    Enregistre une prédiction dans les logs avec horodatage.
    Retourne la chaîne loggée pour audit/test.
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    log_entry = f"[{timestamp}] Input={input_data} → Label={label}, Confidence={confidence:.4f}"
    try:
        logger.info(log_entry)
    except Exception as e:
        logger.error(f"Erreur lors de la journalisation: {e}")
    return log_entry