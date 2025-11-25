# apps/api/security.py
from fastapi import Depends, HTTPException, status
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.security_models import User, Role, ApiKey

SECRET = "CHANGE_ME"
ALGO = "HS256"
EXP_MIN = 60

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def create_token(user: User):
    payload = {"sub": user.email, "role": user.role.value, "exp": datetime.utcnow() + timedelta(minutes=EXP_MIN)}
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def require_role(required: list[Role]):
    def checker(token: str = Depends(lambda x: x), db: Session = Depends(get_db)):
        # Ici, tu récupères le token depuis Authorization: Bearer ...
        # Simplifié: implémenter un extracteur dans ta stack
        try:
            payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        role = Role(payload.get("role"))
        if role not in required:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return payload
    return checker

def require_api_scope(scope: str):
    def checker(api_key: str, db: Session = Depends(get_db)):
        # api_key envoyé via header "X-API-Key"
        ak = db.query(ApiKey).filter_by(active=True).all()
        # Vérifier hash & scopes (simplifié)
        # En prod: compare hash(api_key), puis check scope dans ak.scopes
        return True
    return checker
