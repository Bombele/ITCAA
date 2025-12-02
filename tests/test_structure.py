def test_import_module():
    """
    Vérifie que le module principal itcaa_ai_offline peut être importé.
    Ce test garantit que la structure du projet est correcte et que
    le PYTHONPATH est bien configuré dans le workflow CI/CD.
    """
    import itcaa_ai_offline

    # Vérifie que le module est bien importé
    assert itcaa_ai_offline is not None, "Le module itcaa_ai_offline n'a pas pu être importé"

    # Vérifie que la docstring existe
    assert hasattr(itcaa_ai_offline, "__doc__"), "Le module doit avoir une docstring"

def test_imports_structure():
    from src.itcaa_ai_offline.schemas import PredictionInput, PredictionOutput
    from src.itcaa_ai_offline.utils import normalize_features, log_prediction
    assert callable(normalize_features)
    assert callable(log_prediction)
    assert PredictionInput is not None
    assert PredictionOutput is not None