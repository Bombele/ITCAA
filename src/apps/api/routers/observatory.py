# apps/api/routers/observatory.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models_cartography import Actor, Region, ActorType

router = APIRouter(prefix="/observatory", tags=["observatory"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    counts = {r.value: {t.value: 0 for t in ActorType} for r in Region}
    for r in Region:
        for t in ActorType:
            counts[r.value][t.value] = db.query(Actor).filter(Actor.region==r, Actor.type==t).count()
    return {"portfolio": counts}
