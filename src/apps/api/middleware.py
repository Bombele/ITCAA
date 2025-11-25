# apps/api/middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from apps.api.database import SessionLocal
from apps.api.security_models import AuditEvent

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        db = SessionLocal()
        evt = AuditEvent(
            actor=request.headers.get("X-Actor", "anonymous"),
            action=f"{request.method}",
            resource=str(request.url),
            metadata={"ip": request.client.host, "lang": request.headers.get("Accept-Language")},
            created_at=datetime.utcnow()
        )
        db.add(evt); db.commit(); db.close()
        return response
