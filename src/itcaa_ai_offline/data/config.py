# src/itcaa_ai_offline/data/config.py
from __future__ import annotations
from typing import Any, Dict
from src.itcaa_ai_offline.config import SETTINGS as GLOBAL_SETTINGS

# Synchronisation avec la config globale
SETTINGS: Dict[str, Any] = GLOBAL_SETTINGS.copy()

# Tu peux ajouter des paramètres spécifiques au module data ici
SETTINGS.update({
    "data_cache": "build/cache",
    "repair_mode": "safe",
})