# src/itcaa_ai_offline/routers.py
from __future__ import annotations

from typing import Any, Dict, List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# Exemple de modèle Pydantic pour les requêtes
class Payload(BaseModel):
    text: str


# Exemple de modèle Pydantic pour les réponses
class Prediction(BaseModel):
    label: str
    score: float


@router.post("/predict", response_model=Prediction)
def predict(payload: Payload) -> Prediction:
    """
    Endpoint de prédiction.
    """
    # Exemple de logique : retourne une prédiction factice
    return Prediction(label="example", score=0.99)


@router.get("/health", response_model=Dict[str, str])
def health_check() -> Dict[str, str]:
    """
    Endpoint de vérification de santé.
    """
    return {"status": "ok"}


@router.get("/items", response_model=List[Dict[str, Any]])
def list_items() -> List[Dict[str, Any]]:
    """
    Endpoint qui retourne une liste d'items.
    """
    items: List[Dict[str, Any]] = [
        {"id": 1, "name": "item1"},
        {"id": 2, "name": "item2"},
    ]
    return items