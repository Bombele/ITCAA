# tests/test_predictor.py
import pytest
from itcaa_ai_offline.schemas import PredictionInput, PredictionOutput
from itcaa_ai_offline.predictor import predict

def test_prediction_output_type():
    """
    Vérifie que la fonction predict retourne bien un objet PredictionOutput.
    """
    input_data = PredictionInput(features=[0.5, 1.2, 3.4])
    result = predict(input_data)
    assert isinstance(result, PredictionOutput), "La sortie n'est pas de type PredictionOutput"

def test_prediction_confidence_range():
    """
    Vérifie que le score de confiance est toujours compris entre 0 et 1.
    """
    input_data = PredictionInput(features=[0.1, 0.2, 0.3])
    result = predict(input_data)
    assert 0.0 <= result.confidence <= 1.0, f"Confidence hors plage : {result.confidence}"

def test_prediction_logging(tmp_path, monkeypatch):
    """
    Vérifie que la prédiction est bien journalisée dans le fichier de logs.
    """
    log_file = tmp_path / "ai_offline.log"
    monkeypatch.setenv("LOG_FILE", str(log_file))

    input_data = PredictionInput(features=[0.9, 0.8, 0.7])
    _ = predict(input_data)

    assert log_file.exists(), "Le fichier de log n'a pas été créé"
    content = log_file.read_text()
    assert "Input=" in content, "Le log ne contient pas l'entrée"
    assert "Confidence=" in content, "Le log ne contient pas le score de confiance"
