from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from apps.api.database import SessionLocal
from apps.api.services.tracking_service import check_expiring_mous, check_expiring_mandates
from apps.api.services.notification_service import send_alert_email

router = APIRouter(prefix="/notifications", tags=["notifications"])
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/send-alerts")
async def send_alerts(db: Session = Depends(get_db)):
    mous = check_expiring_mous(db)
    mandates = check_expiring_mandates(db)
    alerts = []
    for m in mous:
        alerts.append(f"MoU avec {m.partner_name} expire le {m.expires_at}")
    for md in mandates:
        alerts.append(f"Mandat du membre {md.member_id} expire le {md.end_date}")

    if not alerts:
        return {"message": "Aucune alerte à envoyer."}

    body_html = templates.get_template("email_alert.html").render(alerts=alerts)
    recipients = ["partners@itcaa.org","council@itcaa.org"]
    return await send_alert_email(recipients, "Alertes ITCAA – Diplomatie", body_html)
