# apps/api/models_actors.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Boolean, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class ActorType(enum.Enum):
    GANE = "gane"        # Groupe armé non étatique
    PMC = "pmc"          # Société militaire privée
    MILITIA = "militia"
    HYBRID = "hybrid"

class Region(enum.Enum):
    AFRICA = "africa"; AMERICAS = "americas"; ASIA = "asia"; EUROPE = "europe"; MENA = "mena"; OCEANIA = "oceania"; GLOBAL = "global"

class Actor(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    type = Column(Enum(ActorType), nullable=False)
    region = Column(Enum(Region), nullable=False)
    active = Column(Boolean, default=True)
    started_at = Column(DateTime)
    notes = Column(String)
    meta = Column(JSON)  # {"aliases": [...], "territorial_control": True, "size_estimate": "1k-5k"}

class ClientCategory(enum.Enum):
    UN = "UN"; UA = "UA"; EU = "EU"; OEA = "OEA"; NGO = "NGO"; STATE = "STATE"; ENTERPRISE = "ENTERPRISE"; THINKTANK = "THINKTANK"

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(Enum(ClientCategory), nullable=False)
    country = Column(String)
    notes = Column(String)

class PartnerType(enum.Enum):
    UNIVERSITY = "UNIVERSITY"; THINKTANK = "THINKTANK"; FOUNDATION = "FOUNDATION"; REGIONAL_ORG = "REGIONAL_ORG"; COMMUNITY = "COMMUNITY"

class Partner(Base):
    __tablename__ = "partners"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(Enum(PartnerType), nullable=False)
    region = Column(Enum(Region), nullable=True)
    notes = Column(String)
    links = Column(JSON)  # {"website": "...", "mou_uri": "..."}

class RiskType(enum.Enum):
    POLITICAL_CONTEST = "political_contest"
    MANIPULATION = "manipulation"
    DATA_SECURITY = "data_security"
    NEUTRALITY = "neutrality"
    DIPLOMACY_FRAGILE = "diplomacy_fragile"

class RiskLevel(enum.Enum):
    LOW = "low"; MEDIUM = "medium"; HIGH = "high"; CRITICAL = "critical"

class RiskRegister(Base):
    __tablename__ = "risk_register"
    id = Column(Integer, primary_key=True)
    risk_type = Column(Enum(RiskType), nullable=False)
    level = Column(Enum(RiskLevel), nullable=False)
    description = Column(String, nullable=False)
    mitigation = Column(String)   # plan d’atténuation
    owner = Column(String)        # responsable
    reviewed_at = Column(DateTime)

class ActorClientLink(Base):
    __tablename__ = "actor_client_links"
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    purpose = Column(String)  # "certification", "assessment", "training"
    status = Column(String, default="active")
    actor = relationship("Actor", backref="client_links")
    client = relationship("Client", backref="actor_links")

class ActorPartnerLink(Base):
    __tablename__ = "actor_partner_links"
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"), nullable=False)
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=False)
    role = Column(String)  # "research_validation", "translation", "regional_gateway"
    actor = relationship("Actor", backref="partner_links")
    partner = relationship("Partner", backref="actor_links")
