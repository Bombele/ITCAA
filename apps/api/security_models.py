# apps/api/security_models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class Role(enum.Enum):
    ADMIN = "admin"
    JURIST = "jurist"
    TECH = "tech"
    DIPLOMAT = "diplomat"
    AUDITOR = "auditor"
    PUBLIC = "public"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    role = Column(Enum(Role), default=Role.PUBLIC)
    is_active = Column(Boolean, default=True)
    mfa_enabled = Column(Boolean, default=False)
    password_hash = Column(String)  # stocke un hash (p.ex. Argon2)
    created_at = Column(DateTime)

class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key_hash = Column(String, unique=True)  # hash du token
    scopes = Column(JSON)  # ["read:reports", "write:evidence"]
    active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    user = relationship("User", backref="api_keys")

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(Integer, primary_key=True)
    actor = Column(String)        # email ou service
    action = Column(String)       # "create_evidence", "update_thresholds"
    resource = Column(String)     # "/certification/1/evidence"
    metadata = Column(JSON)       # {"ip": "...", "lang": "fr", ...}
    created_at = Column(DateTime)

class DataSegment(enum.Enum):
    PUBLIC = "public"
    SENSITIVE = "sensitive"

class DataAsset(Base):
    __tablename__ = "data_assets"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    segment = Column(Enum(DataSegment), default=DataSegment.PUBLIC)
    owner = Column(String)         # "secrétariat technique"
    classification = Column(String)  # "ISO27001-A", "Internal"
    retention_policy = Column(String) # "5y", "indefinite"
