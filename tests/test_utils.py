import os
import pytest
from src.itcaa_ai_offline import utils

def test_normalize_features_numeric():
    features = [10.0, 20.0, 30.0]
    normalized = utils.normalize_features(features)
    assert all(0.0 <= f <= 1.0 for f in normalized)
    assert normalized[0] == 0.0
    assert normalized[-1] == 1.0

def test_normalize_features_mixed():
    features = [10.0, "texte", 30.0]
    normalized = utils.normalize_features(features)
    assert len(normalized) == 2  # ignore le texte
    assert normalized[0] == 0.0
    assert normalized[-1] == 1.0

def test_normalize_features_empty():
    with pytest.raises(ValueError):
        utils.normalize_features([])

def test_log_prediction_creates_log_entry(tmp_path, monkeypatch):
    # Rediriger le dossier logs vers un dossier temporaire
    monkeypatch.setattr(utils, "LOG_DIR", tmp_path)
    os.makedirs(tmp_path, exist_ok=True)

    log_entry = utils.log_prediction([0.1, 0.2], label=1, confidence=0.95)
    assert "Input" in log_entry
    assert "Confidence" in log_entry

    # Vérifier que le fichier de log est créé
    log_file = tmp_path / "ai_offline.log"
    assert log_file.exists()
    content = log_file.read_text()
    assert "Confidence=0.9500" in content
