import torch
import pytest
from pathlib import Path

from src.itcaa_ai_offline import model_loader

def test_model_not_found(tmp_path, monkeypatch):
    # Rediriger MODEL_PATH vers un fichier inexistant
    fake_path = tmp_path / "fake_model.pt"
    monkeypatch.setattr(model_loader, "MODEL_PATH", str(fake_path))

    with pytest.raises(FileNotFoundError):
        model_loader.load_model(path=str(fake_path))

def test_model_load_cpu(tmp_path, monkeypatch):
    # Créer un modèle factice simple
    class DummyModel(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = torch.nn.Linear(2, 1)

        def forward(self, x):
            return self.linear(x)

    dummy_model = DummyModel()
    model_path = tmp_path / "dummy_model.pt"
    torch.save(dummy_model, model_path)

    # Rediriger MODEL_PATH vers ce modèle factice
    monkeypatch.setattr(model_loader, "MODEL_PATH", str(model_path))

    # Charger le modèle sur CPU
    loaded_model = model_loader.load_model(path=str(model_path), device="cpu")
    assert isinstance(loaded_model, DummyModel)
    assert not loaded_model.training, "Le modèle doit être en mode eval()"

def test_device_auto_detection(tmp_path, monkeypatch):
    # Créer un modèle factice
    class DummyModel(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = torch.nn.Linear(2, 1)

        def forward(self, x):
            return self.linear(x)

    dummy_model = DummyModel()
    model_path = tmp_path / "dummy_model.pt"
    torch.save(dummy_model, model_path)

    # Rediriger MODEL_PATH vers ce modèle factice
    monkeypatch.setattr(model_loader, "MODEL_PATH", str(model_path