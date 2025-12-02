import json
import re
from pathlib import Path

# Définition des chemins vers les fichiers générés par l'index
META_FILE = Path("src/itcaa_ai_offline/data/index/meta.json")
REPORT_FILE = Path("src/itcaa_ai_offline/data/index/index_report.md")

def test_index_report_exists():
    # Vérifie que le rapport existe
    assert REPORT_FILE.exists(), "Le fichier index_report.md est manquant."

def test_index_report_structure():
    content = REPORT_FILE.read_text(encoding="utf-8")
    # Vérifie que les sections principales existent
    assert "# 📊 Rapport Index ITCAA" in content
    assert "## 🔎 Détails corpus" in content
    assert "## 📝 Auditabilité" in content

def test_index_report_consistency_with_meta():
    meta = json.loads(META_FILE.read_text(encoding="utf-8"))
    content = REPORT_FILE.read_text(encoding="utf-8")

    # Vérifie cohérence du nombre de passages
    assert f"**Nombre total de passages indexés** : {meta['total_passages']}" in content

    # Vérifie cohérence du modèle
    assert meta["embedding_model"] in content

    # Vérifie cohérence du paramètre top_k
    assert str(meta["top_k_default"]) in content

    # Vérifie cohérence des langues détectées
    for lang in meta["languages_detected"]:
        assert lang