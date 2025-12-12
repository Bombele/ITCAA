# src/itcaa_ai_offline/models/capsules.py
from __future__ import annotations

from typing import List
from pydantic import BaseModel  # type: ignore


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