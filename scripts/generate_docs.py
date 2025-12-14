import os
import subprocess
from datetime import datetime

def list_branches():
    """Liste toutes les branches distantes du dépôt."""
    raw = subprocess.check_output(["git", "branch", "-r"]).decode().splitlines()
    return [b.strip().replace("origin/", "") for b in raw if "origin/" in b]

def list_files_in_folder(folder):
    """Retourne les fichiers Markdown présents dans un dossier."""
    files = []
    for file in os.listdir(folder):
        if file.endswith(".md"):
            files.append(file)
    return files

def generate_module_guide():
    """Génère MODULE_GUIDE.md avec les modules et fichiers Markdown par branche."""
    lines = ["# MODULE_GUIDE.md\n"]
    lines.append(f"_Dernière génération : {datetime.now().isoformat()}_\n\n")
    for branch in list_branches():
        lines.append(f"## Branche : {branch}\n")
        subprocess.run(["git", "checkout", branch], check=True)
        for folder in os.listdir():
            if os.path.isdir(folder) and folder not in [".git", ".github", "scripts"]:
                lines.append(f"- `{folder}/` → module détecté dans `{branch}`")
                md_files = list_files_in_folder(folder)
                for md in md_files:
                    lines.append(f"  - `{md}`")
        lines.append("")
    return "\n".join(lines)

def generate_index_guide():
    """Génère INDEX_GUIDE.md avec les liens vers onboarding et modules par branche."""
    lines = ["# INDEX_GUIDE.md\n"]
    lines.append(f"_Dernière génération : {datetime.now().isoformat()}_\n\n")
    lines.append("## Onboarding\n")
    lines.append("- [Débutant](ONBOARDING_BEGINNER.md)")
    lines.append("- [Intermédiaire](ONBOARDING_INTERMEDIATE.md)")
    lines.append("- [Expert](ONBOARDING_EXPERT.md)\n")
    lines.append("## Modules par branche\n")
    for branch in list_branches():
        anchor = branch.replace("/", "-")
        lines.append(f"- `{branch}` → voir [MODULE_GUIDE.md](MODULE_GUIDE.md#branche-{anchor})")
    return "\n".join(lines)

if __name__ == "__main__":
    with open("MODULE_GUIDE.md", "w") as f:
        f.write(generate_module_guide())
    with open("INDEX_GUIDE.md", "w") as f:
        f.write(generate_index_guide())
    print("✅ Documentation synchronisée avec toutes les branches et fichiers Markdown listés")