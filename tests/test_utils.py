import os
import pytest
from src.itcaa_ai_offline import utils

def test_normalize_features_numeric():
    # Cas classique : uniquement des valeurs numériques
    features = [10.0, 20.0, 30.0]
    normalized = utils.normalize_features(features)
    assert all(0.0 <= f <= 1.0 for f in normalized), "Toutes les valeurs doivent être normalisées entre 0 et 1"
    assert normalized[0] == 0.0, "La première valeur doit être normalisée à 0.0"
    assert normalized[-1] == 1.0, "La dernière valeur doit être normalisée à 1.0"

def test_normalize_features_mixed():
    # Cas mixte : valeurs numériques et texte
    features = [10.0, "texte", 30.0]
    normalized = utils.normalize_features(features)
    assert len(normalized) == 2, "Les valeurs non numériques doivent être ignorées"
    assert normalized[0] == 0.0
    assert normalized[-1] == 1.0

def test_normalize_features_empty():
    # Cas d'erreur : liste vide
    with pytest.raises(ValueError, match="Features list is empty"):
        utils.normalize_features([])

def test_log_prediction_creates_log_entry(tmp_path, monkeypatch):
    # Rediriger le dossier logs vers un dossier temporaire
    monkeypatch.setattr(utils, "LOG_DIR", tmp_path)
    os.makedirs(tmp_path, exist_ok=True)

    log_entry = utils.log_prediction([0.1, 0.2], label=1, confidence=0.95)

    # Vérifier que le log contient les informations attendues
    assert "Input" in log_entry
    assert "Confidence" in log_entry

    # Vérifier que le fichier de log est bien créé
    log_file = tmp_path / "ai_offline.log"
    assert log_file.exists(), "Le fichier de log n'a pas été créé"
    content = log_file.read_text(encoding="utf-8")
    assert "Confidence=0.9500" in content, "Le contenu du log