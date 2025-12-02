import pytest
from src.itcaa_ai_offline.schemas import PredictionInput, PredictionOutput

def test_prediction_input_numeric():
    # Cas classique : features numériques
    data = PredictionInput(features=[0.1, 0.2, 0.3])
    assert all(isinstance(f, float) for f in data.features), "Toutes les features doivent être des floats"

def test_prediction_input_textual():
    # Cas semantic : features textuelles
    data = PredictionInput(features=["Bonjour ITCAA"])
    assert all(isinstance(f, str) for f in data.features), "Toutes les features doivent être des strings"

def test_prediction_output_classifier():
    # Sortie mode classifier
    output = PredictionOutput(label=1, confidence=0.95)
    assert isinstance(output.label, int), "Le label doit être un entier"
    assert 0 <= output.confidence <= 1, "La confiance doit être comprise entre 0 et 1"

def test_prediction_output_semantic():
    # Sortie mode semantic avec metadata
    output = PredictionOutput(
        label="Réponse basée sur la base locale:\n- Bonjour ITCAA.",
        confidence=1.0,
        metadata={"top_k": 5, "lang": "fr"}
    )
    assert isinstance(output.label, str), "Le label doit être une chaîne de caractères"
    assert output.metadata["lang"] == "fr", "La langue doit être correctement définie dans metadata"

def test_prediction_output_error():
    # Sortie avec erreur
    output = PredictionOutput(
        label="Erreur",
        confidence=0.0,
        error="Index FAISS introuvable"
    )
    assert output.error == "Index FAISS introuvable", "Le message d'erreur doit être cohérent"