# apps/api/policy_service.py
import yaml
from pathlib import Path

def load_security_policies():
    return yaml.safe_load(Path("configs/security_policies.yml").read_text(encoding="utf-8"))

def role_requires_mfa(role: str) -> bool:
    p = load_security_policies()
    return role in p["access"]["mfa_required_roles"]
