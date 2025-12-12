# src/itcaa_ai_offline/health_check.py
from __future__ import annotations

from typing import Dict
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", response_model=Dict[str, str])
def health_check() -> Dict[str, str]:
    """
    Endpoint de vérification de santé.
    """
    return {"status": "ok"}