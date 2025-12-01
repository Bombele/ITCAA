# src/init_db.py
import logging
from apps.api.database import init_db, SessionLocal
from apps.api.models.models_actors import Actor, ActorType, Region, Client, ClientCategory, Partner, PartnerType

# 📌 Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("ITCAA_DB_Init")

def seed_data():
    db = SessionLocal()
    try:
        # Exemple d’acteurs
        actors = [
            Actor(name="Alpha PMC", type=ActorType.PMC, region=Region.AFRICA),
            Actor(name="Militia Verde", type=ActorType.MILITIA, region=Region.AMERICAS),
            Actor(name="Hybrid Force", type=ActorType.HYBRID, region=Region.ASIA),
        ]

        # Exemple de clients
        clients = [
            Client(name="ONU", category=ClientCategory.UN, country="Global"),
            Client(name="Union Africaine", category=ClientCategory.UA, country="Africa"),
            Client(name="ONG Human Rights Watch", category=ClientCategory.NGO, country="Global"),
        ]

        # Exemple de partenaires
        partners = [
            Partner(name="Université de Bruxelles", type=PartnerType.UNIVERSITY, region=Region.EUROPE),
            Partner(name="ThinkTank Global Policy", type=PartnerType.THINKTANK, region=Region.GLOBAL),
        ]

        # ✅ Protection contre doublons
        for obj in actors + clients + partners:
            exists = db.query(obj.__class__).filter_by(name=obj.name).first()
            if not exists:
                db.add(obj)

        db.commit()
        logger.info("✅ Données initiales insérées avec succès")
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erreur lors de l’insertion des données : {e}")
        return False

    finally:
        db.close()

if __name__ == "__main__":
    logger.info("🔧 Initialisation de la base ITCAA...")
    init_db()
    success = seed_data()
    if success:
        logger.info("🚀 Base ITCAA prête avec données de test")
    else:
        logger.warning("⚠️ Base ITCAA initialisée mais avec erreurs")
