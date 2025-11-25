# apps/api/routers/map.py
@router.get("/actors/{actor_id}/geojson")
def actor_geojson(actor_id: int):
    features = load_actor_geojson(actor_id)  # zones d'opération, sites civils, couloirs humanitaires
    return {"type": "FeatureCollection", "features": features}
