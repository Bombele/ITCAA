from pathlib import Path

def test_multilingue_corpus():
    # Chemin vers ton fichier combiné multilingue
    corpus_file = Path("src/itcaa_ai_offline/data/corpus/fondamentaux_itcaa_multilingue.txt")
    assert corpus_file.exists(), "Le fichier combiné multilingue n'existe pas"

    text = corpus_file.read_text(encoding="utf-8")

    # Vérifier que chaque langue ONU est présente
    required_langs = ["[FR]", "[EN]", "[ES]", "[RU]", "[ZH]", "[AR]"]
    for lang in required_langs:
        assert lang in text, f"Corpus incomplet : section {lang} manquante"

    # Vérifier que chaque section est bien structurée
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