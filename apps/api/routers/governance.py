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
# apps/api/routers/governance.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.governance_models import AdvisoryMember, EthicsCase, AuditExternal, FundingDisclosure
from apps.api.security import require_role
from apps.api.security_models import Role

router = APIRouter(prefix="/governance", tags=["governance"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/advisory/members")
def list_members(db: Session = Depends(get_db)):
    return db.query(AdvisoryMember).filter_by(active=True).all()

@router.post("/advisory/members")
def add_member(payload: dict, db: Session = Depends(get_db), _=Depends(require_role([Role.ADMIN]))):
    m = AdvisoryMember(**payload); db.add(m); db.commit(); db.refresh(m); return m

@router.get("/ethics/cases")
def list_ethics(db: Session = Depends(get_db)):
    return db.query(EthicsCase).all()

@router.post("/ethics/cases")
def open_ethics(payload: dict, db: Session = Depends(get_db), _=Depends(require_role([Role.JURIST, Role.ADMIN]))):
    c = EthicsCase(**payload); db.add(c); db.commit(); db.refresh(c); return c

@router.get("/audits/external")
def list_audits(db: Session = Depends(get_db)):
    return db.query(AuditExternal).all()

@router.post("/audits/external")
def add_audit(payload: dict, db: Session = Depends(get_db), _=Depends(require_role([Role.AUDITOR, Role.ADMIN]))):
    a = AuditExternal(**payload); db.add(a); db.commit(); db.refresh(a); return a

@router.get("/funding/disclosures")
def funding_public(db: Session = Depends(get_db)):
    return db.query(FundingDisclosure).filter_by(public=True).all()

@router.post("/funding/disclosures")
def add_funding(payload: dict, db: Session = Depends(get_db), _=Depends(require_role([Role.ADMIN]))):
    f = FundingDisclosure(**payload); db.add(f); db.commit(); db.refresh(f); return f
# apps/api/routers/governance.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.governance_models import AdvisoryMember
from apps.api.schemas.governance import AdvisoryMemberCreate, AdvisoryMemberOut

router = APIRouter(prefix="/governance", tags=["governance"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/advisory/members", response_model=AdvisoryMemberOut)
def add_member(payload: AdvisoryMemberCreate, db: Session = Depends(get_db)):
    m = AdvisoryMember(**payload.dict())
    db.add(m); db.commit(); db.refresh(m)
    return m
# apps/api/routers/governance.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models_governance import AdvisoryMember, AdvisoryReport

router = APIRouter(prefix="/governance", tags=["governance"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/advisory/members")
def list_members(db: Session = Depends(get_db)):
    return db.query(AdvisoryMember).filter_by(active=True).all()

@router.post("/advisory/members")
def add_member(payload: dict, db: Session = Depends(get_db)):
    m = AdvisoryMember(**payload)
    db.add(m); db.commit(); db.refresh(m)
    return m

@router.get("/advisory/reports")
def list_reports(db: Session = Depends(get_db)):
    return db.query(AdvisoryReport).filter_by(public=True).all()

@router.post("/advisory/reports")
def add_report(payload: dict, db: Session = Depends(get_db)):
    r = AdvisoryReport(**payload)
    db.add(r); db.commit(); db.refresh(r)
    return r
