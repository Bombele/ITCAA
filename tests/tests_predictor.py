import pytest
from src.itcaa_ai_offline.predictor import Predictor


def test_predictor_initialization():
    predictor = Predictor(model_path="models/test_model")
    assert predictor is not None
    assert isinstance(predictor, Predictor)


def test_predictor_predict_single_input():
    predictor = Predictor(model_path="models/test_model")
    result = predictor.predict("Bonjour")
    assert isinstance(result, dict)
    assert "label" in result
    assert "confidence" in result


def test_predictor_predict_batch_inputs():
    predictor = Predictor(model_path="models/test_model")
    inputs = ["Bonjour", "Salut", "Hello"]
    results = predictor.predict_batch(inputs)
    assert isinstance(results, list)
    assert len(results) == len(inputs)
    assert all("label" in r and "confidence" in r for r in results)


def test_predictor_invalid_input():
    predictor = Predictor(model_path="models/test_model")
    with pytest.raises(ValueError, match="Invalid input type"):
        predictor.predict(123)


def test_predictor_save_and_load(tmp_path):
    predictor = Predictor(model_path="models/test_model")
    save_path = tmp_path / "predictor_state.json"
    predictor.save(str(save_path))

    new_predictor = Predictor(model_path="models/test_model")
    new_predictor.load(str(save_path))

    result = new_predictor.predict("Bonjour")
    assert "label" in result
    assert "confidence" in result