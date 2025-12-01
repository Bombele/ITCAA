# src/itcaa_ai_offline/schemas.py
from pydantic import BaseModel, Field
from typing import List, Union, Optional, Any

class PredictionInput(BaseModel):
    features: List[Union[float, str]] = Field(
        ...,
        description="Caractéristiques d’entrée : valeurs numériques (mode classifier) ou texte (mode semantic)."
    )

class PredictionOutput(BaseModel):
    label: Union[int, str] = Field(
        ...,
        description="Classe prédite (int, mode classifier) ou réponse textuelle (str, mode semantic)."
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Score de confiance associé à la prédiction."
    )
    metadata: Optional[Any] = Field(
        None,
        description="Informations supplémentaires (ex: passages FAISS, logs, device utilisé)."
    )
    error: Optional[str] = Field(
        None,
        description="Message d’erreur si la prédiction échoue."
    )
