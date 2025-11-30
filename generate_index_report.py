import json
import faiss
from datetime import datetime
from src.itcaa_ai_offline import config

def generate_index_report():
    # Charger l'index FAISS
    index = faiss.read_index(str(config.PATHS.faiss_index))
    meta = json.loads(config.PATHS.meta_json.read_text(encoding="utf-8"))

    # Détecter les langues (simple heuristique par caractères Unicode)
    def detect_lang(text):
        if any("\u0600" <= ch <= "\u06FF" for ch in text): return "Arabe"
        if any("\u4E00" <= ch <= "\u9FFF" for ch in text): return "Chinois"
        if any("\u0400" <= ch <= "\u04FF" for ch in text): return "Russe"
        if any(ch in "áéíóúñ" for ch in text.lower()): return "Espagnol"
        if any(ch in "àâçéèêëîïôûùüÿ" for ch in text.lower()): return "Français"
        return "Anglais"

    languages = {detect_lang(m["text"]) for m in meta}

    # Construire le rapport Markdown
    report = f"""# 📊 Rapport Index ITCAA

- **Date de dernière reconstruction** : {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC
- **Nombre total de passages indexés** : {len(meta)}
- **Nombre total de vecteurs FAISS** : {index.ntotal}
- **Langues détectées dans le corpus** : {", ".join(sorted(languages))}

## 🔎 Détails corpus
"""
    for i, m in enumerate(meta[:10], 1):  # afficher les 10 premiers passages
        report += f"- Passage {i}: {m['text'][:60]}...\n"

    # Sauvegarder le rapport
    (config.PATHS.index_dir / "index_report.md").write_text(report, encoding="utf-8")
    print("✅ Rapport index_report.md généré.")

if __name__ == "__main__":
    generate_index_report()