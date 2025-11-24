# apps/api/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
import enum

class OrgType(enum.Enum):
    UN = "UN"; UA = "UA"; EU = "EU"; OEA = "OEA"; NGO = "NGO"; University = "University"; ThinkTank = "ThinkTank"; Other = "Other"

class PartnerOrg(Base):
    __tablename__ = "partner_orgs"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    org_type = Column(Enum(OrgType), nullable=False)
    country = Column(String)
    notes = Column(String)

class SupportLetter(Base):
    __tablename__ = "support_letters"
    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("partner_orgs.id"), nullable=False)
    title = Column(String)
    uri = Column(String)    # lien document
    issued_at = Column(DateTime)
    partner = relationship("PartnerOrg", backref="letters")

class CommunityInput(Base):
    __tablename__ = "community_inputs"
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, index=True)
    locale = Column(String, default="fr")
    content = Column(String)   # commentaire citoyen
    evidence_uri = Column(String)
    created_at = Column(DateTime)
