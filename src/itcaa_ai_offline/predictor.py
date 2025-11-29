# predictor.py
from model_loader import load_model
from schemas import PredictionInput, PredictionOutput
from utils import normalize_features, log_prediction
import torch

# Charger le modèle IA hors ligne
model = load_model()

def predict(input_data: PredictionInput) -> PredictionOutput:
    # 🧹 Normalisation des données d’entrée
    normalized_features = normalize_features(input_data.features)

    # Conversion en tenseur
    input_tensor = torch.tensor([normalized_features], dtype=torch.float32)

    # Prédiction
    with torch.no_grad():
        output = model(input_tensor)

    # Traitement du résultat
    prediction = output.argmax(dim=1).item()
    confidence = torch.nn.functional.softmax(output, dim=1)[0][prediction].item()

    # 📝 Journalisation pour auditabilité
    log_prediction(input_data.features, prediction, confidence)

    return PredictionOutput(
        label=prediction,
        confidence=round(confidence, 4)
    )

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Tuple
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from .config import PATHS, EMBEDDING_MODEL, TOP_K

class OfflinePredictor:
    def __init__(self) -> None:
        if not PATHS.faiss_index.exists() or not PATHS.meta_json.exists():
            raise FileNotFoundError("Index FAISS ou meta.json manquants. Construisez l'index avant prédiction.")
        self.index = faiss.read_index(str(PATHS.faiss_index))
        self.meta = json.loads(PATHS.meta_json.read_text(encoding="utf-8"))
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def search(self, query: str, k: int = TOP_K) -> List[Tuple[float, dict]]:
        if not query.strip():
            return []
        q_vec = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype("float32")
        scores, ids = self.index.search(q_vec, k)
        results: List[Tuple[float, dict]] = []
        for score, idx in zip(scores[0].tolist(), ids[0].tolist()):
            if idx == -1:
                continue
            results.append((float(score), self.meta[idx]))
        return results

    def answer(self, query: str, k: int = TOP_K) -> str:
        hits = self.search(query, k=k)
        if not hits:
            return "Aucune information disponible dans la base locale."
        # Assemblage simple: prend les meilleurs passages et compose une réponse courte
        parts = [f"- {m['text']}" for _, m in hits]
        return "Réponse basée sur la base locale:\n" + "\n".join(parts)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m itcaa_ai_offline.predictor \"votre question\"")
        raise SystemExit(1)
    query = " ".join(sys.argv[1:])
    predictor = OfflinePredictor()
    print(predictor.answer(query))
