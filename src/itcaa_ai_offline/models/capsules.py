from __future__ import annotations

from typing import ClassVar, Dict, List, Optional
from pydantic import BaseModel, Field


class Capsule(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)

    # Store en mémoire (à remplacer par DB)
    _store: ClassVar[Dict[int, "Capsule"]] = {}

    @classmethod
    def get_all(cls) -> List["Capsule"]:
        """
        Retourne toutes les capsules.
        """
        return list(cls._store.values())

    @classmethod
    def get_by_id(cls, capsule_id: int) -> Optional["Capsule"]:
        """
        Retourne une capsule par identifiant.
        """
        return cls._store.get(capsule_id)

    @classmethod
    def create(cls, payload: "CapsuleCreate") -> "Capsule":
        """
        Crée une capsule à partir d'un payload CapsuleCreate.
        Génère un id incrémental simple.
        """
        next_id = (max(cls._store.keys()) + 1) if cls._store else 1
        capsule = Capsule(id=next_id, title=payload.title, description=payload.description)
        cls._store[next_id] = capsule
        return capsule

    @classmethod
    def delete(cls, capsule_id: int) -> bool:
        """
        Supprime une capsule par identifiant.
        """
        if capsule_id in cls._store:
            del cls._store[capsule_id]
            return True
        return False


class CapsuleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)