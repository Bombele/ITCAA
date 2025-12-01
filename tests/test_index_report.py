import json
import re
from pathlib import Path

META_FILE = Path("src/itcaa_ai_offline/index/meta.json")
REPORT_FILE = Path("src/itcaa_ai_offline/index/index_report.md")

def test_index_report_exists():
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
        assert lang.lower() in content.lower()

def test_index_report_date_format():
    content = REPORT_FILE.read_text(encoding="utf-8")
    # Vérifie que la date est au format ISO ou UTC
    assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC", content), \
        "La date de reconstruction doit être au format YYYY-MM-DD HH:MM:SS UTC"

def test_index_report_status():
    content = REPORT_FILE.read_text(encoding="utf-8")
    # Vérifie que le statut CI/CD est présent
    assert "Statut de validation CI/CD" in content
    assert "Validé" in content or "Invalid" in content or "Pending" in content