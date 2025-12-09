#!/usr/bin/env python3
"""
validate_render_config.py
Vérifie la cohérence de la configuration Render (render.yaml) et la structure src/.
Institutionnalisation pour CI/CD ITCAA.
"""

import sys
import os
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
RENDER_FILE = ROOT / "render.yaml"

def log(msg: str):
    print(f"🔍 [validate-render] {msg}", flush=True)

def check_render_file() -> bool:
    """Vérifie que render.yaml existe et est lisible."""
    if not RENDER_FILE.exists():
        log("❌ Fichier render.yaml manquant.")
        return False
    try:
        with open(RENDER_FILE, "r", encoding="utf-8") as f:
            yaml.safe_load(f)
        log("✅ Fichier render.yaml présent et valide YAML.")
        return True
    except yaml.YAMLError as e:
        log(f"❌ Erreur de syntaxe YAML dans render.yaml → {e}")
        return False
    except Exception as e:
        log(f"❌ Erreur inattendue lors de la lecture de render.yaml → {e}")
        return False

def check_src_structure() -> bool:
    """Vérifie que le dossier src contient les modules critiques."""
    ok = True
    required_dirs = ["apps", "itcaa_ai_offline"]
    for d in required_dirs:
        path = SRC / d
        if not path.exists():
            log(f"❌ Dossier manquant : {path}")
            ok = False
        else:
            log(f"✅ Dossier présent : {path}")
    return ok

def main():
    log("Démarrage de la validation Render…")
    ok = True
    if not check_render_file():
        ok = False
    if not check_src_structure():
        ok = False

    if ok:
        log("🎯 Configuration Render valide. Prêt pour CI/CD.")
        sys.exit(0)
    else:
        log("🚫 Configuration Render invalide. Corrige avant déploiement.")
        sys.exit(1)

if __name__ == "__main__":
    main()