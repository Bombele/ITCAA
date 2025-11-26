import os
import yaml

def check_file(path):
    if os.path.isfile(path):
        print(f"✅ Fichier {path} trouvé")
        return True
    else:
        print(f"❌ Fichier {path} manquant")
        print(f"➡️ Suggestion : créer ou restaurer {path}")
        return False

def check_folder(path):
    if os.path.isdir(path):
        print(f"✅ Dossier {path}/ trouvé")
        return True
    else:
        print(f"❌ Dossier {path}/ manquant")
        print(f"➡️ Suggestion : créer le dossier {path}/")
        return False

def check_render_yaml():
    path = "render.yaml"
    if not check_file(path):
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        start_cmd = data.get("startCommand", "")
        expected = "PYTHONPATH=src python -m uvicorn apps.api.main:app --host 0.0.0.0 --port $PORT"
        if start_cmd.strip() == expected:
            print("✅ startCommand correct dans render.yaml")
            return True
        else:
            print("❌ startCommand incorrect dans render.yaml")
            print(f"➡️ Actuel : {start_cmd}")
            print(f"➡️ Attendu : {expected}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de render.yaml : {e}")
        return False

def main():
    print("🔍 Validation de la configuration Render
