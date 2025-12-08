#!/bin/bash

echo "📦 Installation de Poetry..."

# Installer Poetry via le script officiel
curl -sSL https://install.python-poetry.org | python3 -

# Ajouter Poetry au PATH
export PATH="$HOME/.local/bin:$PATH"

# Vérifier que Poetry est bien installé
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry n'est pas disponible après installation"
    exit 1
fi

# Afficher la version
echo "✅ Poetry installé : $(poetry --version)"

# Installer le plugin export
echo "🔌 Installation du plugin poetry-plugin-export..."
poetry self add poetry-plugin-export

# Vérifier que la commande export est disponible
if poetry export --help | grep -q "Export the dependencies"; then
    echo "✅ Plugin export installé avec succès"
else
    echo "❌ Échec de l'installation du plugin export"
    exit 1
fi

echo "🎉 Setup Poetry terminé avec succès"