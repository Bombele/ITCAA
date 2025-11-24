# apps/api/schemas/security.py
from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    jurist = "jurist"
    tech = "tech"
    diplomat = "diplomat"
    auditor = "auditor"
    public = "public"

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    role: Role = Role.public
    password: constr(min_length=8)
    mfa_enabled: bool = False

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: Role
    is_active: bool
    mfa_enabled: bool

    class Config:
        orm_mode = True

class ApiKeyCreate(BaseModel):
    user_id: int
    scopes: List[str]

class ApiKeyOut(BaseModel):
    id: int
    user_id: int
    scopes: List[str]
    active: bool

    class Config:
        orm_mode = True

class AuditEventOut(BaseModel):
    id: int
    actor: str
    action: str
    resource: str
    metadata: dict
    created_at: str

    class Config:
        orm_mode = True
