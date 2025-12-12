import pytest
from fastapi.testclient import TestClient
from src.apps.api.routers.capsules import router
from src.itcaa_ai_offline.models import Capsule, CapsuleCreate
from fastapi import FastAPI

# Créer une app FastAPI pour tester le router
app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_list_capsules_initially_empty():
    response = client.get("/capsules/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_capsule():
    payload = {"title": "Capsule 1", "description": "Première capsule"}
    response = client.post("/capsules/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Capsule 1"
    assert data["description"] == "Première capsule"
    assert "id" in data


def test_get_capsule_by_id():
    # Créer une capsule
    payload = {"title": "Capsule 2", "description": "Deuxième capsule"}
    create_response = client.post("/capsules/", json=payload)
    capsule_id = create_response.json()["id"]

    # Récupérer la capsule
    response = client.get(f"/capsules/{capsule_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == capsule_id
    assert data["title"] == "Capsule 2"


def test_delete_capsule():
    # Créer une capsule
    payload = {"title": "Capsule 3", "description": "Troisième capsule"}
    create_response = client.post("/capsules/", json=payload)
    capsule_id = create_response.json()["id"]

    # Supprimer la capsule
    delete_response = client.delete(f"/capsules/{capsule_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "deleted"

    # Vérifier que la capsule n'existe plus
    get_response = client.get(f"/capsules/{capsule_id}")
    assert get_response.status_code == 404