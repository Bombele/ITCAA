import subprocess
import sys

def run_command(cmd: list[str]) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution de {cmd}: {e.stderr}")
        sys.exit(1)

def main():
    print("🔍 Vérification des dépendances Python...")

    # Vérification de cohérence avec pip
    print("\n=== Étape 1 : pip check ===")
    pip_check_output = run_command([sys.executable, "-m", "pip", "check"])
    if pip_check_output.strip():
        print(pip_check_output)
    else:
        print("✅ Aucune incohérence détectée avec pip check.")

    # Arbre des dépendances
    print("\n=== Étape 2 : pipdeptree ===")
    try:
        pipdeptree_output = run_command([sys.executable, "-m", "pipdeptree"])
        print(pipdeptree_output)
    except SystemExit:
        print("⚠️ pipdeptree non installé. Installez-le avec `pip install pipdeptree`.")

    print("\n✅ Validation des dépendances terminée.")

if __name__ == "__main__":
    main()