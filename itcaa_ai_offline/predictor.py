# predictor.py
from model_loader import load_model
from schemas import PredictionInput, PredictionOutput
import torch

model = load_model()

def predict(input_data: PredictionInput) -> PredictionOutput:
    # Convertir les données en tenseur
    input_tensor = torch.tensor([input_data.features], dtype=torch.float32)
    
    # Prédiction
    with torch.no_grad():
        output = model(input_tensor)
    
    # Traitement du résultat
    prediction = output.argmax(dim=1).item()
    confidence = torch.nn.functional.softmax(output, dim=1)[0][prediction].item()
    
    return PredictionOutput(
        label=prediction,
        confidence=round(confidence, 4)
  )
