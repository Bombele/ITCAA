# apps/api/routers/governance.py
from fastapi import APIRouter
router = APIRouter(prefix="/governance", tags=["governance"])

@router.get("/partners")
def list_partners():
    # return orgs + letters
    ...

@router.post("/partners")
def add_partner(payload: dict):
    ...

@router.get("/support-letters")
def list_support_letters():
    ...
