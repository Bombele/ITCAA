import os
import sys

# 📁 Dossiers et fichiers à vérifier
structure = {
    "src": ["__init__.py"],
    "src/apps": ["__init__.py"],
    "src/apps/api": ["__init__.py", "main.py"],
}

errors = []  # collecte des erreurs pour résumé final


def check_path(path: str, files: list[str]) -> None:
    """Vérifie la présence d'un dossier et des fichiers attendus."""
    full_path = os.path.join(*path.split("/"))
    if os.path.isdir(full_path):
        print(f"✅ Dossier {path}/ trouvé")
        for f in files:
            file_path = os.path.join(full_path, f)
            if os.path.isfile(file_path):
                print(f"✅ Fichier {path}/{f} trouvé")
            else:
                msg = f"❌ Fichier {path}/{f} manquant"
                print(msg)
                print(f"➡️ Suggestion : créer le fichier {path}/{f}")
                errors.append(msg)
    else:
        msg = f"❌ Dossier {path}/ manquant"
        print(msg)
        print(f"➡️ Suggestion : créer le dossier {path}/ avec les fichiers {', '.join(files)}")
        errors.append(msg)


def main() -> None:
    print("🔍 Vérification de la structure du projet ITCAA\n")
    for path, files in structure.items():
        check_path(path, files)

    print("\n📊 Résumé de la vérification :")
    if errors:
        print(f"❌ {len(errors)} problème(s) détecté(s)")
        for e in errors:
            print(f"   - {e}")
        sys.exit(1)  # code de sortie non nul en cas d'erreurs
    else:
        print("✅ Structure complète et conforme")
        sys.exit(0)


if __name__ == "__main__":
    main()
