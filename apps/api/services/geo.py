import json
from pathlib import Path
from db import models
from shapely.geometry import shape, Point

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

# 🚀 Nueva función: verificar si un actor está dentro de un polígono GeoJSON
def actor_in_polygon(actor: models.Actor, polygon_geojson: dict) -> bool:
    """
    Verifica si el actor (usando su geojson de coordenadas) está dentro de un polígono.
    - actor.geojson debe contener {"type": "Point", "coordinates": [lon, lat]}
    - polygon_geojson debe ser un Feature o Geometry válido de tipo Polygon/MultiPolygon
    """
    if not actor.geojson:
        return False

    try:
        actor_point = shape(actor.geojson)  # convierte el geojson del actor en Point
        polygon = shape(polygon_geojson)    # convierte el geojson del polígono en Polygon/MultiPolygon
        return polygon.contains(actor_point)
    except Exception as e:
        print(f"Error en verificación espacial: {e}")
        return False
