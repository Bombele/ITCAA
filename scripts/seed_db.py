import json
from sqlalchemy.orm import Session
from apps.api.db.session import SessionLocal
from apps.api.db import models

def seed_actors(db: Session, path="data/seeds/actors_seed.json"):
    with open(path, "r", encoding="utf-8") as f:
        actors_data = json.load(f)

    for actor_data in actors_data:
        # Créer l'acteur
        actor = models.Actor(
            id=actor_data["id"],
            name=actor_data["name"],
            acronym=actor_data["acronym"],
            typology=actor_data["typology"],
            country=actor_data["country"],
            region=actor_data["region"],
            geojson=actor_data["geojson"]
        )
        db.add(actor)
        db.commit()
        db.refresh(actor)

        # Ajouter les engagements liés
        for e in actor_data.get("engagements", []):
            engagement = models.Engagement(
                actor_id=actor.id,
                category=e["category"],
                description=e["description"]
            )
            db.add(engagement)
        db.commit()


def seed_criteria(db: Session, path="data/seeds/criteria_seed.json"):
    with open(path, "r", encoding="utf-8") as f:
        criteria_data = json.load(f)

    for c in criteria_data:
        criterion = models.Criterion(
            id=c["id"],
            name=c["name"],
            category=c["category"],
            description=c["description"],
            weight=c["weight"]
        )
        db.add(criterion)
    db.commit()


def seed_capsules(db: Session, path="data/seeds/capsules_seed.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            capsules_data = json.load(f)

        for cap in capsules_data:
            capsule = models.Capsule(
                id=cap["id"],
                actor_id=cap["actor_id"],
                protocol=cap["protocol"],
                score=cap["score"],
                version=cap.get("version", "v1.0")
            )
            db.add(capsule)
        db.commit()
    except FileNotFoundError:
        print("⚠️ Aucun fichier capsules_seed.json trouvé, étape ignorée.")


def run_seed():
    db: Session = SessionLocal()
    print("🌱 Initialisation de la base ITCAA...")

    seed_actors(db)
    print("✅ Acteurs insérés.")

    seed_criteria(db)
    print("✅ Critères insérés.")

    seed_capsules(db)
    print("✅ Capsules insérées (si fichier présent).")

    print("🎉 Base ITCAA initialisée avec succès.")


if __name__ == "__main__":
    run_seed()
