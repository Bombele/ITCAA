import pytest
import src  # fonctionne si src/__init__.py existe et PYTHONPATH est défini

def test_version_and_metadata():
    # Vérifie que les métadonnées sont présentes
    assert hasattr(src, "__version__"), "La version doit être définie dans src"
    assert isinstance(src.__version__, str)
    assert hasattr(src, "__author__"), "L'auteur doit être défini dans src"
    assert hasattr(src, "__license__"), "La licence doit être définie dans src"

def test_all_exports():
    # Vérifie que __all__ expose les bons modules
    expected_exports = {
        "PredictionInput",
        "PredictionOutput",
        "OfflinePredictor",
        "normalize_features",
        "log_prediction",
        "router",
    }
    assert set(src.__all__) == expected_exports

def test_imports_work():
    # Vérifie que les modules exposés sont accessibles directement depuis src
    from src import (
        PredictionInput,
        PredictionOutput,
        OfflinePredictor,
        normalize_features,
        log_prediction,
        router,
    )

    assert PredictionInput is not None
    assert PredictionOutput is not None
    assert OfflinePredictor is not None
    assert callable(normalize_features)
    assert callable(log_prediction)
    assert router is not None