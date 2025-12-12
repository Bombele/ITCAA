# src/itcaa_ai_offline/schemas.py
from __future__ import annotations

# Ignorer les erreurs MyPy sur pydantic si les stubs ne sont pas disponibles
from pydantic import BaseModel  # type: ignore
from typing import List


class Capsule(BaseModel):  # type: ignore
    """
    Représente une capsule avec un identifiant, un texte et un embedding.
    """
    id: str
    text: str
    embedding: List[float]


class CapsuleBatch(BaseModel):  # type: ignore
    """
    Représente un lot de capsules.
    """
    capsules: List[Capsule]