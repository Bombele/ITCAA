# apps/api/routers/forums.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models_forums import ForumPresence

router = APIRouter(prefix="/forums", tags=["forums"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/")
def list_forums(db: Session = Depends(get_db)):
    return db.query(ForumPresence).all()
