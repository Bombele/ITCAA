from pathlib import Path
import yaml
from db import models
from services import dih_score, legitimacy

# Ruta base de los diccionarios
DICTIONARIES_PATH = Path("data/dictionaries")

def load_yaml(file_name: str):
    file_path = DICTIONARIES_PATH / file_name
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def calculate_certification(actor: models.Actor):
    """
    Calcula el score de certificación de un actor combinando DIH y legitimidad.
    """

    # Calcular los scores parciales
    dih = dih_score.compute_dih_score(actor)
    legit = legitimacy.compute_legitimacy_score(actor)

    # Fórmula de certificación (ajustable con pesos)
    certification_score = round((dih * 0.5 + legit * 0.5), 2)

    # Crear cápsula automática
    capsule = models.Capsule(
        actor_id=actor.id,
        narrative=f"Certificación calculada para {actor.name}",
        legitimacy_score=legit,
        dih_score=dih,
        certification_score=certification_score,
        version="v1.0",
        validations=[{"source": "ITCAA", "status": "calculado"}],
    )

    return capsule, certification_score
