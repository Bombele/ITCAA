from pathlib import Path

CORPUS_FILE = Path("src/itcaa_ai_offline/data/corpus/fondamentaux_itcaa_multilingue.txt")

def test_multilingue_corpus_exists():
    # Vérifie que le fichier combiné multilingue existe
    assert CORPUS_FILE.exists(), "Le fichier combiné multilingue est manquant"

def test_multilingue_corpus_languages():
    text = CORPUS_FILE.read_text(encoding="utf-8")

    # Vérifier que chaque langue officielle de l'ONU est présente
    required_langs = ["[FR]", "[EN]", "[ES]", "[RU]", "[ZH]", "[AR]"]
    for lang in required_langs:
        assert lang in text, f"Corpus incomplet : section {lang} manquante"

def test_multilingue_corpus_sections():
    text = CORPUS_FILE.read_text(encoding="utf-8")

    # Vérifier que chaque section thématique est bien structurée
    sections = [
        "Section 1 : Culture afro-latine",
        "Section 2 : Charte des Nations Unies",
        "Section 3 : Conventions de Genève (1949)",
        "Section 4 : Principes du DIH",
        "Section 5 : Introduction aux droits humains",
        "Section 6 : Jurisprudence de la Cour pénale internationale",
        "Section 7 : Mécanismes des Nations Unies",
        "Section 8 : Tendances urbaines contemporaines",
    ]
    for section in sections:
        assert section in text, f"Corpus incomplet : {section} manquante"