from pathlib import Path

CORPUS_DIR = Path("src/itcaa_ai_offline/data/corpus")
CORPUS_FILE = CORPUS_DIR / "afro_latine_culture.txt"

def test_corpus_file_exists():
    assert CORPUS_FILE.exists(), "Le fichier corpus n'existe pas"

def test_corpus_not_empty():
    text = CORPUS_FILE.read_text(encoding="utf-8").strip()
    assert len(text) > 0, "Le corpus est vide"

def test_corpus_lines_reasonable():
    lines = [l.strip() for l in CORPUS_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert all(len(l) < 300 for l in lines), "Certaines lignes sont trop longues (>300 caractères)"

def test_all_corpus_files():
    files = list(CORPUS_DIR.glob("*.txt"))
    assert files, "Aucun fichier corpus trouvé"

    for f in files:
        text = f.read_text(encoding="utf-8").strip()
        assert text, f"Le fichier {f.name} est vide"
        assert len(text) > 20, f"Le fichier {f.name} est trop court"