import pytest
from fastapi.testclient import TestClient
from src.itcaa_ai_offline.routers import router
from fastapi import FastAPI

# Créer une app FastAPI minimale pour tester le router
app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_predict_classifier(monkeypatch):
    # Mock du prédicteur classifier pour éviter dépendances lourdes
    from src.itcaa_ai_offline import predictor

    class DummyPredictor:
        def predict(self, input_data):
            return predictor.PredictionOutput(label=1, confidence=0.95)

    monkeypatch.setattr(predictor, "OfflinePredictor", lambda mode="classifier": DummyPredictor())

    response = client.post(
        "/predict?mode=classifier",
        json={"features": [0.1, 0.2, 0.3]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "confidence" in data
    assert data["label"] == 1
    assert 0 <= data["confidence"] <= 1


def test_predict_semantic(monkeypatch):
    # Mock du prédicteur semantic
    from src.itcaa_ai_offline import predictor

    class DummyPredictor:
        def answer(self, query, k=5):
            return "Réponse basée sur la base locale:\n- Bonjour ITCAA."

    monkeypatch.setattr(predictor, "OfflinePredictor", lambda mode="semantic": DummyPredictor())

    response = client.post(
        "/predict?mode=semantic",
        json={"features": ["Bonjour ITCAA"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "confidence" in data
    assert "Bonjour ITCAA" in data["label"]
    assert data["confidence"] == 1.0