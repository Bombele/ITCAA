# tests/test_corpus.py
from pathlib import Path

def test_corpus_file_exists():
    path = Path("src/itcaa_ai_offline/data/corpus/afro_latine_culture.txt")
    assert path.exists(), "Le fichier corpus n'existe pas"

def test_corpus_not_empty():
    text = Path("src/itcaa_ai_offline/data/corpus/afro_latine_culture.txt").read_text(encoding="utf-8")
    assert len(text.strip()) > 0, "Le corpus est vide"

def test_corpus_lines_reasonable():
    text = Path("src/itcaa_ai_offline/data/corpus/afro_latine_culture.txt").read_text(encoding="utf-8")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    assert all(len(l) < 300 for l in lines), "Certaines lignes sont trop longues (>300 caractères)"
# tests/test_corpus.py
from pathlib import Path

def test_all_corpus_files():
    corpus_dir = Path("src/itcaa_ai_offline/data/corpus")
    files = list(corpus_dir.glob("*.txt"))
    assert files, "Aucun fichier corpus trouvé"

    for f in files:
        text = f.read_text(encoding="utf-8").strip()
        assert text, f"Le fichier {f.name} est vide"
        assert len(text) > 20, f"Le fichier {f.name} est trop court"