# apps/api/econ_models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

class RevenueType(enum.Enum):
    CERTIFICATION = "certification"
    TRAINING = "training"
    CONSULTING = "consulting"
    PUBLICATION = "publication"
    LICENSE = "license"
    GRANT = "grant"

class CostType(enum.Enum):
    INFRASTRUCTURE = "infrastructure"
    MAINTENANCE = "maintenance"
    MULTILINGUAL = "multilingual"
    TEAM = "team"
    DIPLOMACY = "diplomacy"
    COMMUNICATION = "communication"
    OTHER = "other"

class ContractStatus(enum.Enum):
    PIPELINE = "pipeline"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Revenue(Base):
    __tablename__ = "revenues"
    id = Column(Integer, primary_key=True)
    type = Column(Enum(RevenueType), nullable=False)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)     # USD
    currency = Column(String, default="USD")
    period = Column(String, default="annual")  # monthly / quarterly / annual / one-off
    org_name = Column(String)                  # client/donor
    notes = Column(String)
    recorded_at = Column(DateTime)

class Cost(Base):
    __tablename__ = "costs"
    id = Column(Integer, primary_key=True)
    type = Column(Enum(CostType), nullable=False)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)     # USD
    currency = Column(String, default="USD")
    period = Column(String, default="annual")
    notes = Column(String)
    recorded_at = Column(DateTime)

class EconContract(Base):
    __tablename__ = "econ_contracts"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)      # e.g., "Consulting UA 2026"
    client = Column(String, nullable=False)
    type = Column(Enum(RevenueType), nullable=False)
    value = Column(Float, nullable=False)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    status = Column(Enum(ContractStatus), default=ContractStatus.PIPELINE)
    signed = Column(Boolean, default=False)

class EconProjection(Base):
    __tablename__ = "econ_projections"
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    expected_revenue = Column(Float, default=0.0)
    expected_costs = Column(Float, default=0.0)
    scenario = Column(String, default="baseline")  # baseline / optimistic / conservative
    notes = Column(String)
