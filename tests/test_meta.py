import json
import re
import pytest
from pathlib import Path

META_FILE = Path("src/itcaa_ai_offline/index/meta.json")

def test_meta_file_exists():
    assert META_FILE.exists(), "Le fichier meta.json est manquant."

def test_meta_structure():
    data = json.loads(META_FILE.read_text())

    # Champs obligatoires
    required_fields = [
        "index_version",
        "last_updated",
        "total_passages",
        "languages_detected",
        "embedding_model",
        "top_k_default",
        "corpus_files",
        "audit"
    ]
    for field in required_fields:
        assert field in data, f"Champ manquant dans meta.json: {field}"

def test_last_updated_format():
    data = json.loads(META_FILE.read_text())
    last_updated = data["last_updated"]
    # Vérifie format ISO 8601
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", last_updated), \
        "last_updated doit être au format ISO 8601 (UTC)."

def test_total_passages_consistency():
    data = json.loads(META_FILE.read_text())
    total_passages = data["total_passages"]
    corpus_files = data["corpus_files"]
    assert isinstance(total_passages, int) and total_passages >= 0
    assert isinstance(corpus_files, list) and all(isinstance(f, str) for f in corpus_files)

def test_audit_section():
    data = json.loads(META_FILE.read_text())
    audit = data["audit"]
    assert "generated_by" in audit
    assert "report_file" in audit
    assert "status" in audit
    assert audit["status"] in ["valid", "invalid", "pending"]