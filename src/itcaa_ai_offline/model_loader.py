import torch
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Définir chemin modèle (configurable via variable d'environnement)
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = os.getenv("ITCAA_MODEL_PATH", str(MODELS_DIR / "model.pt"))

def load_model(path: str = MODEL_PATH, device: str = None):
    """
    Charge un modèle PyTorch depuis le chemin donné.
    - path : chemin du fichier modèle (.pt)
    - device : "cpu" ou "cuda" (auto-détection si None)
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Modèle introuvable à l’emplacement : {path}")

    # Détection automatique du device
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    try:
        logging.info(f"Chargement du modèle depuis {path} sur {device}...")
        model = torch.load(path, map_location=torch.device(device))
        model.eval()
        logging.info("✅ Modèle chargé et mis en mode évaluation.")
        return model
    except Exception as e:
        logging.error(f"Erreur lors du chargement du modèle : {e}")
        raise RuntimeError(f"Impossible de charger le modèle : {e}")
