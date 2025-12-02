import pytest
from pathlib import Path
from itcaa_ai_offline.utils import normalize_features, log_prediction
from itcaa_ai_offline.schemas import PredictionInput, PredictionOutput
from itcaa_ai_offline.config import PATHS
from itcaa_ai_offline.index_builder import build_index
from itcaa_ai_offline.predictor import OfflinePredictor

def test_normalize_features_basic():
    features = [10, 20, 30]
    normalized = normalize_features(features)
    assert normalized == [0.0, 0.5, 1.0]

def test_normalize_features_identical_values():
    features = [5, 5, 5]
    normalized = normalize_features(features)
    assert normalized == [0.0, 0.0, 0.0]

def test_log_prediction_creates_log(tmp_path, monkeypatch):
    log_file = tmp_path / "ai_offline.log"
    monkeypatch.setenv("LOG_FILE", str(log_file))

    input_data = PredictionInput(features=[0.1, 0.2, 0.3])
    output_data = PredictionOutput(label="A", confidence=0.85)

    log_prediction(input_data.features, output_data.label, output_data.confidence)

    assert log_file.exists()
    content = log_file.read_text()
    assert "Input=" in content
    assert "Confidence=" in content

def setup_module(module=None):
    # Construit l'index avant les tests si absent
    if (not PATHS.faiss_index.exists()) or (not PATHS.meta_json.exists()):
        build_index()

def test_answer_non_empty():
    predictor = OfflinePredictor()
    ans = predictor.answer("Quels sont les principes du DIH ?")
    assert "Réponse basée sur la base locale" in ans or "⚠️" in ans

def test_empty_query():
    predictor = OfflinePredictor()
    hits = predictor.search("")
    assert hits == []

def test_query_specificity():
    predictor = OfflinePredictor()
    hits = predictor.search("ONU mécanismes")
    if hits:
        assert all(-1.0 <= s <= 1.0 for s, _ in hits)

def test_semantic_answer():
    predictor = OfflinePredictor(mode="semantic")
    result = predictor.answer("Quels sont les principes du DIH ?")
    assert isinstance(result, str)
    assert "Réponse basée sur la base locale" in result or "⚠️" in result

def test_semantic_search():
    predictor = OfflinePredictor(mode="semantic")
    results = predictor.search("humanitaire", k=3)
    assert isinstance(results, list)
    if results:
        score, meta = results[0]
        assert isinstance(score, float)
        assert isinstance(meta, dict)

def test_classifier_predict():
    predictor = OfflinePredictor(mode="classifier")
    dummy_input = PredictionInput(features=[0.1, 0.2, 0.3])
    output = predictor.predict(dummy_input)
    assert hasattr(output, "label")
    assert hasattr(output, "confidence")
    assert isinstance(output.label, int)
    assert isinstance(output.confidence, float)
    assert 0.0 <= output.confidence <= 1.0