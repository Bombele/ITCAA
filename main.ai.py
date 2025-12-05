from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from pathlib import Path
from src.itcaa_ai_offline.core import ai_engine

# 📊 Configurer les logs
LOGFILE = Path("logs/main_ai_api.log")
LOGFILE.parent.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# 🚀 Initialiser l'application FastAPI
app = FastAPI(title="ITCAA AI Offline API", version="1.0.0")

# 📥 Modèle de requête
class PredictionRequest(BaseModel):
    text: str

# 📤 Modèle de réponse
class PredictionResponse(BaseModel):
    result: str

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Endpoint pour exécuter une prédiction IA."""
    if not request.text.strip():
        logging.error("Entrée vide reçue")
        raise HTTPException(status_code=400, detail="Texte d'entrée invalide")

    try:
        result = ai_engine.process(request.text)
        logging.info("Prédiction IA exécutée avec succès")
        return PredictionResponse(result=result)
    except Exception as e:
        logging.exception("Erreur lors de la prédiction IA")
        raise HTTPException(status_code=500, detail=f"Erreur interne : {e}")

# Endpoint de santé
@app.get("/health")
def health_check():
    """Vérifie que l'API est opérationnelle."""
    return {"status": "ok", "message": "ITCAA AI Offline API fonctionne correctement"}
