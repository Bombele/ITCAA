import os

# 📁 Dossiers et fichiers à vérifier
structure = {
    "src": ["__init__.py"],
    "src/apps": ["__init__.py"],
    "src/apps/api": ["__init__.py", "main.py"]
}

def check_path(path, files):
    full_path = os.path.join(*path.split("/"))
    if os.path.isdir(full_path):
        print(f"✅ Dossier {path}/ trouvé")
        for f in files:
            file_path = os.path.join(full_path, f)
            if os.path.isfile(file_path):
                print(f"✅ Fichier {path}/{f} trouvé")
            else:
                print(f"❌ Fichier {path}/{f} manquant")
                print(f"➡️ Suggestion : créer le fichier {path}/{f}")
    else:
        print(f"❌ Dossier {path}/ manquant")
        print(f"➡️ Suggestion : créer le dossier {path}/ avec les fichiers {', '.join(files)}")

def main():
    print("🔍 Vérification de la structure du projet ITCAA\n")
    for path, files in structure.items():
        check_path(path, files)

if __name__ == "__main__":
    main()
