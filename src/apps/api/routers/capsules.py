from fastapi import APIRouter, HTTPException
from typing import List
from src.itcaa_ai_offline.models import Capsule, CapsuleCreate

router = APIRouter(
    prefix="/capsules",
    tags=["capsules"],
)


@router.get("/", response_model=List[Capsule])
def list_capsules() -> List[Capsule]:
    """
    Retourne la liste des capsules disponibles.
    """
    return Capsule.get_all()


@router.get("/{capsule_id}", response_model=Capsule)
def get_capsule(capsule_id: int) -> Capsule:
    """
    Retourne une capsule par son identifiant.
    """
    capsule = Capsule.get_by_id(capsule_id)
    if capsule is None:
        raise HTTPException(status_code=404, detail="Capsule not found")
    return capsule


@router.post("/", response_model=Capsule)
def create_capsule(capsule: CapsuleCreate) -> Capsule:
    """
    Crée une nouvelle capsule.
    """
    return Capsule.create(capsule)


@router.delete("/{capsule_id}", response_model=dict)
def delete_capsule(capsule_id: int) -> dict:
    """
    Supprime une capsule par son identifiant.
    """
    success = Capsule.delete(capsule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Capsule not found")
    return {"status": "deleted"}