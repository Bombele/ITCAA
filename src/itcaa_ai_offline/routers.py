# src/itcaa_ai_offline/routers.py
from fastapi import APIRouter, HTTPException, Query
from .schemas import PredictionInput, PredictionOutput
from .predictor import OfflinePredictor

router = APIRouter()

# Initialisation par défaut en mode classifier
predictor_classifier = OfflinePredictor(mode="classifier")
predictor_semantic = OfflinePredictor(mode="semantic")

@router.post("/predict", response_model=PredictionOutput)
def get_prediction(
    input_data: PredictionInput,
    mode: str = Query("classifier", enum=["classifier", "semantic"])
):
    """
    Endpoint REST pour obtenir une prédiction IA hors ligne.
    - mode="classifier" → classification supervisée Torch
    - mode="semantic" → recherche sémantique FAISS
    """
    try:
        if mode == "classifier":
            return predictor_classifier.predict(input_data)
        elif mode == "semantic":
            # On renvoie une réponse textuelle basée sur FAISS
            answer = predictor_semantic.answer(" ".join(map(str, input_data.features)))
            return PredictionOutput(label=answer, confidence=1.0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur prédiction: {e}")
