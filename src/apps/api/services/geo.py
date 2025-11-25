from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import session, models
from services import geo

router = APIRouter()

# Dépendance pour obtenir la session DB
def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint pour récupérer les pays
@router.get("/countries")
def get_countries():
    return geo.get_countries()

# Endpoint pour récupérer les régions
@router.get("/regions")
def get_regions():
    return geo.get_regions()

# Endpoint combiné
@router.get("/all")
def get_all_geo():
    return {
        "countries": geo.get_countries(),
        "regions": geo.get_regions()
    }

# 🚀 Nouveau endpoint : acteurs dans une région
@router.get("/actors/in-region/{region_name}")
def actors_in_region(region_name: str, db: Session = Depends(get_db)):
    regions = geo.get_regions()

    # Chercher la région par nom
    region_feature = None
    for feature in regions["features"]:
        if feature["properties"].get("name") == region_name:
            region_feature = feature
            break

    if not region_feature:
        raise HTTPException(status_code=404, detail=f"Région {region_name} non trouvée")

    # Vérifier quels acteurs sont dans le polygone
    actors = db.query(models.Actor).all()
    inside = []
    for actor in actors:
        if actor.geojson and geo.actor_in_polygon(actor, region_feature["geometry"]):
            inside.append({
                "id": actor.id,
                "name": actor.name,
                "country": actor.country,
                "region": actor.region,
                "geojson": actor.geojson
            })

    return {"region": region_name, "actors_inside": inside}
import json
from pathlib import Path
from db import models
from shapely.geometry import shape

# Ruta base de los archivos geo
GEO_PATH = Path("data/geo")

def load_geojson(file_name: str):
    file_path = GEO_PATH / file_name
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo {file_name} no encontrado en {GEO_PATH}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_countries():
    return load_geojson("countries.geojson")

def get_regions():
    return load_geojson("regions.geojson")

def filter_actors_by_country(db, country_name: str):
    return db.query(models.Actor).filter(models.Actor.country == country_name).all()

def filter_actors_by_region(db, region_name: str):
    return db.query(models.Actor).filter(models.Actor.region == region_name).all()

def actor_in_polygon(actor: models.Actor, polygon_geojson: dict) -> bool:
    """
    Vérifie si l'acteur est dans un polygone GeoJSON.
    - actor.geojson doit être un Point {"type": "Point", "coordinates": [lon, lat]}
    - polygon_geojson doit être un Polygon/MultiPolygon
    """
    if not actor.geojson:
        return False
    try:
        actor_point = shape(actor.geojson)
        polygon = shape(polygon_geojson)
        return polygon.contains(actor_point)
    except Exception as e:
        print(f"Erreur géospatiale: {e}")
        return False
