from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models.models_actors import Client
from apps.api.schemas.schemas_actors import ClientCreate, ClientRead

router = APIRouter(prefix="/clients", tags=["Clients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ClientRead])
def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).order_by(Client.name).all()

@router.post("/", response_model=ClientRead, status_code=201)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    client = Client(**payload.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.get("/{client_id}", response_model=ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client
