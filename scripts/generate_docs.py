import os
import subprocess
from datetime import datetime

def list_branches():
    """Retourne la liste de toutes les branches distantes."""
    branches = subprocess.check_output(["git", "branch", "-r"]).decode().splitlines()
    return [b.strip().replace("origin/", "") for b in branches if "origin/" in b]

def generate_module_guide():
    """Génère MODULE_GUIDE.md avec les modules par branche."""
    lines = ["# MODULE_GUIDE.md\n"]
    lines.append(f"_Dernière génération : {datetime.now().isoformat()}_\n\n")
    for branch in list_branches():
        lines.append(f"## Branche: {branch}\n")
        # Checkout de la branche pour explorer son contenu
        subprocess.run(["git", "checkout", branch], check=True)
        for folder in os.listdir(os.getcwd()):
            if os.path.isdir(folder) and folder not in [".git", ".github", "scripts"]:
                lines.append(f"- `{folder}/` → module présent dans la branche `{branch}`")
        lines.append("\n")
    return "\n".join(lines)

def generate_index_guide():
    """Génère INDEX_GUIDE.md avec liens vers onboarding et modules par branche."""
    lines = ["# INDEX_GUIDE.md\n"]
    lines.append(f"_Dernière génération : {datetime.now().isoformat()}_\n\n")
    lines.append("## Onboarding\n")
    lines.append("- [Débutant](ONBOARDING_BEGINNER.md)\n")
    lines.append("- [Intermédiaire](ONBOARDING_INTERMEDIATE.md)\n")
    lines.append("- [Expert](ONBOARDING_EXPERT.md)\n\n")
    lines.append("## Modules par branche\n")
    for branch in list_branches():
        anchor = branch.replace("/", "-")  # pour créer un lien Markdown valide
        lines.append(f"- {branch} → voir [MODULE_GUIDE.md](MODULE_GUIDE.md#branche-{anchor})\n")
    return "\n".join(lines)

if __name__ == "__main__":
    with open("MODULE_GUIDE.md", "w") as f:
        f.write(generate_module_guide())
    with open("INDEX_GUIDE.md", "w") as f:
        f.write(generate_index_guide())
    print("✅ Documentation générée et synchronisée avec toutes les branches")