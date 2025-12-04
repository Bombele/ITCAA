import json
import faiss
from datetime import datetime
from pathlib import Path
from src.itcaa_ai_offline import config
import sys

def detect_lang(text: str) -> str:
    """Détection heuristique de la langue par caractères Unicode."""
    if not text:
        return "Inconnu"
    if any("\u0600" <= ch <= "\u06FF" for ch in text): return "Arabe"
    if any("\u4E00" <= ch <= "\u9FFF" for ch in text): return "Chinois"
    if any("\u0400" <= ch <= "\u04FF" for ch in text): return "Russe"
    if any(ch in "áéíóúñ" for ch in text.lower()): return "Espagnol"
    if any(ch in "àâçéèêëîïôûùüÿ" for ch in text.lower()): return "Français"
    return "Anglais"

def generate_index_report():
    try:
        # Vérifier existence des fichiers
        if not config.PATHS.faiss_index.exists():
            print(f"❌ Index FAISS introuvable : {config.PATHS.faiss_index}")
            sys.exit(1)
        if not config.PATHS.meta_json.exists():
            print(f"❌ Fichier meta.json introuvable : {config.PATHS.meta_json}")
            sys.exit(1)

        # Charger l'index FAISS
        index = faiss.read_index(str(config.PATHS.faiss_index))

        # Charger les métadonnées
        try:
            meta = json.loads(config.PATHS.meta_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"❌ Erreur JSON dans meta.json : {e}")
            sys.exit(1)

        if not isinstance(meta, list):
            print("❌ Format invalide : meta.json doit contenir une liste")
            sys.exit(1)

        # Détecter les langues
        languages = {detect_lang(m.get("text", "")) for m in meta if isinstance(m, dict)}

        # Construire le rapport Markdown
        report = f"""# 📊 Rapport Index ITCAA

- **Date de dernière reconstruction** : {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC
- **Nombre total de passages indexés** : {len(meta)}
- **Nombre total de vecteurs FAISS** : {index.ntotal}
- **Langues détectées dans le corpus** : {", ".join(sorted(languages))}

## 🔎 Détails corpus
"""
        for i, m in enumerate(meta[:10], 1):  # afficher les 10 premiers passages
            text = m.get("text", "")
            report += f"- Passage {i}: {text[:60]}...\n"

        # Sauvegarder le rapport
        output_file = config.PATHS.index_dir / "index_report.md"
        Path(output_file).write_text(report, encoding="utf-8")
        print(f"✅ Rapport généré : {output_file}")

    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_index_report()
