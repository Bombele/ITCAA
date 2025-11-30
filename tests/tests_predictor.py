# tests/test_utils.py
import pytest
from itcaa_ai_offline.utils import normalize_features, log_prediction
from itcaa_ai_offline.schemas import PredictionInput, PredictionOutput

def test_normalize_features_basic():
    """
    Vérifie que la normalisation transforme les valeurs entre 0 et 1.
    """
    features = [10, 20, 30]
    normalized = normalize_features(features)
    assert normalized == [0.0, 0.5, 1.0], f"Résultat inattendu : {normalized}"

def test_normalize_features_identical_values():
    """
    Vérifie que des valeurs identiques sont normalisées à 0.0.
    """
    features = [5, 5, 5]
    normalized = normalize_features(features)
    assert normalized == [0.0, 0.0, 0.0], f"Résultat inattendu : {normalized}"

def test_log_prediction_creates_log(tmp_path, monkeypatch):
    """
    Vérifie que log_prediction écrit bien dans le fichier LOG_FILE.
    """
    log_file = tmp_path / "ai_offline.log"
    monkeypatch.setenv("LOG_FILE", str(log_file))

    input_data = PredictionInput(features=[0.1, 0.2, 0.3])
    output_data = PredictionOutput(prediction="A", confidence=0.85)

    log_prediction(input_data, output_data)

    assert log_file.exists(), "Le fichier de log n'a pas été créé"
    content = log_file.read_text()
    assert "Input=" in content, "Le log ne contient pas l'entrée"
    assert "Confidence=" in content, "Le log ne contient pas le score de confiance"

import os
from pathlib import Path
from itcaa_ai_offline.config import PATHS
from itcaa_ai_offline.index_builder import build_index
from itcaa_ai_offline.predictor import OfflinePredictor

def setup_module(module=None):
    # Construit l'index avant les tests si absent
    if (not PATHS.faiss_index.exists()) or (not PATHS.meta_json.exists()):
        build_index()

def test_answer_non_empty():
    predictor = OfflinePredictor()
    ans = predictor.answer("Quels sont les principes du DIH ?")
    assert "Réponse basée sur la base locale" in ans
    assert len(ans.splitlines()) >= 2

def test_empty_query():
    predictor = OfflinePredictor()
    hits = predictor.search("")
    assert hits == []

def test_query_specificity():
    predictor = OfflinePredictor()
    hits = predictor.search("ONU mécanismes")
    assert len(hits) >= 1
    # score doit être entre -1 et 1 (cosinus)
    assert all(-1.0 <= s <= 1.0 for s, _ in hits)

import pytest
from itcaa_ai_offline.predictor import OfflinePredictor
from itcaa_ai_offline.schemas import PredictionInput


def test_semantic_answer():
    """
    Vérifie que le mode semantic retourne une réponse non vide
    quand on interroge le corpus local.
    """
    predictor = OfflinePredictor(mode="semantic")
    result = predictor.answer("Quels sont les principes du DIH ?")
    assert isinstance(result, str)
    assert "Réponse basée sur la base locale" in result or "⚠️" in result


def test_semantic_search():
    """
    Vérifie que la recherche FAISS retourne une liste de tuples (score, meta).
    """
    predictor = OfflinePredictor(mode="semantic")
    results = predictor.search("humanitaire", k=3)
    assert isinstance(results, list)
    if results:  # si corpus non vide
        score, meta = results[0]
        assert isinstance(score, float)
        assert isinstance(meta, dict)


def test_classifier_predict():
    """
    Vérifie que le mode classifier retourne un PredictionOutput
    avec label et confiance.
    """
    predictor = OfflinePredictor(mode="classifier")
    dummy_input = PredictionInput(features=[0.1, 0.2, 0.3])  # exemple simple
    output = predictor.predict(dummy_input)
    assert hasattr(output, "label")
    assert hasattr(output, "confidence")
    assert isinstance(output.label, int)
    assert isinstance(output.confidence, float)
    assert 0.0 <= output.confidence <= 1.0

from __future__ import annotations
import json
import logging
from typing import List, Tuple
import numpy as np
import faiss
import torch
from sentence_transformers import SentenceTransformer
from .config import PATHS, EMBEDDING_MODEL, TOP_K
from .model_loader import load_model   # ✅ correction import
from .schemas import PredictionInput, PredictionOutput
from .utils import normalize_features, log_prediction

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class OfflinePredictor:
    """
    IA hors ligne hybride : recherche sémantique (FAISS) ou classification supervisée (Torch).
    """

    def __init__(self, mode: str = "semantic") -> None:
        self.mode = mode
        if self.mode == "semantic":
            self._init_semantic()
        elif self.mode == "classifier":
            self._init_classifier()
        else:
            raise ValueError(f"Mode inconnu: {self.mode}")

    def _init_semantic(self) -> None:
        if not PATHS.faiss_index.exists():
            raise FileNotFoundError(f"Index FAISS introuvable: {PATHS.faiss_index}")
        if not PATHS.meta_json.exists():
            raise FileNotFoundError(f"Métadonnées introuvables: {PATHS.meta_json}")

        try:
            self.index = faiss.read_index(str(PATHS.faiss_index))
            self.meta = json.loads(PATHS.meta_json.read_text(encoding="utf-8"))
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            logging.info("✅ Mode semantic initialisé avec FAISS et SentenceTransformer.")
        except Exception as e:
            logging.error(f"Erreur initialisation semantic: {e}")
            raise

    def _init_classifier(self) -> None:
        try:
            self.model = load_model()
            logging.info("✅ Mode classifier initialisé avec Torch.")
        except Exception as e:
            logging.error(f"Erreur initialisation classifier: {e}")
            raise

    def search(self, query: str, k: int = TOP_K) -> List[Tuple[float, dict]]:
        if not query.strip():
            logging.warning("⚠️ Requête vide.")
            return []

        q_vec = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        # Limiter k au nombre de vecteurs disponibles
        k = min(k, len(self.meta))

        scores, ids = self.index.search(q_vec, k)
        results: List[Tuple[float, dict]] = []

        for score, idx in zip(scores[0].tolist(), ids[0].tolist()):
            if idx == -1 or idx >= len(self.meta):
                continue
            results.append((float(score), self.meta[idx]))

        logging.info(f"🔎 Recherche '{query}' → {len(results)} résultats.")
        return results

    def answer(self, query: str, k: int = TOP_K) -> str:
        hits = self.search(query, k=k)
        if not hits:
            return "⚠️ Aucune information disponible dans la base locale."
        parts = [f"- {m['text']}" for _, m in hits]
        return "Réponse basée sur la base locale:\n" + "\n".join(parts)

    def predict(self, input_data: PredictionInput) -> PredictionOutput:
        features = normalize_features(input_data.features)
        input_tensor = torch.tensor([features], dtype=torch.float32)

        try:
            with torch.no_grad():
                output = self.model(input_tensor)

            prediction = output.argmax(dim=1).item()
            confidence = torch.nn.functional.softmax(output, dim=1)[0][prediction].item()

            log_prediction(input_data.features, prediction, confidence)

            logging.info(f"🧮 Prédiction: label={prediction}, confiance={confidence:.4f}")
            return PredictionOutput(
                label=prediction,
                confidence=round(confidence, 4)
            )
        except Exception as e:
            logging.error(f"Erreur lors de la prédiction: {e}")
            raise RuntimeError(f"Impossible de générer une prédiction: {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m itcaa_ai_offline.predictor \"votre question\"")
        raise SystemExit(1)

    query = " ".join(sys.argv[1:])
    predictor = OfflinePredictor(mode="semantic")
    print(predictor.answer(query))