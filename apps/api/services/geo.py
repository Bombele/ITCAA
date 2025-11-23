import json
from pathlib import Path
from db import models

# Ruta base de los archivos geo
GEO_PATH = Path("data/geo")

def load_geojson(file_name: str):
    """
    Carga un archivo GeoJSON desde la carpeta data/geo.
    """
    file_path = GEO_PATH / file_name
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo {file_name} no encontrado en {GEO_PATH}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_countries():
    """
    Devuelve el GeoJSON de países.
    """
    return load_geojson("countries.geojson")

def get_regions():
    """
    Devuelve el GeoJSON de regiones.
    """
    return load_geojson("regions.geojson")

def filter_actors_by_country(db, country_name: str):
    """
    Filtra actores por país.
    """
    return db.query(models.Actor).filter(models.Actor.country == country_name).all()

def filter_actors_by_region(db, region_name: str):
    """
    Filtra actores por región.
    """
    return db.query(models.Actor).filter(models.Actor.region == region_name).all()
