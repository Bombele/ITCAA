# apps/api/models_tracking.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class MoU(Base):
    __tablename__ = "mous"
    id = Column(Integer, primary_key=True)
    partner_name = Column(String, nullable=False)
    signed_at = Column(DateTime)
    expires_at = Column(DateTime)
    active = Column(Boolean, default=True)
    notes = Column(String)

class Mandate(Base):
    __tablename__ = "mandates"
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("advisory_members.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    active = Column(Boolean, default=True)
    member = relationship("AdvisoryMember", backref="mandates")
