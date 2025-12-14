import os
from datetime import datetime

def list_files_in_folder(folder):
    """Retourne les fichiers Markdown et Python présents dans un dossier."""
    files = []
    for file in os.listdir(folder):
        if file.endswith(".md") or file.endswith(".py"):
            files.append(file)
    return files

def generate_module_guide():
    """Génère MODULE_GUIDE.md avec les modules et fichiers de la branche active."""
    lines = ["# MODULE_GUIDE.md\n"]
    lines.append(f"_Dernière génération : {datetime.now().isoformat()}_\n\n")
    lines.append("## Branche : main\n")
    for folder in os.listdir():
        if os.path.isdir(folder) and folder not in [".git", ".github", "scripts"]:
            lines.append(f"- `{folder}/` → module détecté dans `main`")
            md_files = list_files_in_folder(folder)
            for md in md_files:
                lines.append(f"  - `{md}`")
    # Ajouter aussi les fichiers à la racine
    lines.append("\n### Fichiers à la racine\n")
    for file in os.listdir():
        if os.path.isfile(file) and (file.endswith(".md") or file.endswith(".py")):
            lines.append(f"- `{file}`")
    return "\n".join(lines)

if __name__ == "__main__":
    with open("MODULE_GUIDE.md", "w") as f:
        f.write(generate_module_guide())
    print("✅ MODULE_GUIDE.md mis à jour avec les fichiers de la branche main")