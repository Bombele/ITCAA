# 🧱 Étape 1 : Image de base légère pour build
FROM python:3.12-slim AS builder

# 🔧 Variables d’environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# 📦 Installer dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl python3-venv python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 📦 Installer Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# 🔌 Vérifier que Poetry est bien installé
RUN poetry --version

# 🔌 Installer le plugin poetry-plugin-export
RUN poetry self add poetry-plugin-export

# 📂 Copier les fichiers de config
COPY pyproject.toml poetry.lock* ./

# 📦 Exporter les requirements
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt \
    && poetry export -f requirements.txt --without-hashes --with dev -o requirements-dev.txt

# 🧱 Étape 2 : Image finale
FROM python:3.12-slim

# 🔧 Variables d’environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=prod \
    PYTHONPATH=/app/src \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# 🛠️ Installer dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential xz-utils \
    && rm -rf /var/lib/apt/lists/*

# 📂 Copier les requirements exportés
COPY --from=builder /app/requirements.txt /app/requirements.txt
COPY src/itcaa_ai_offline/requirements-ai.txt ./requirements-ai.txt

# 📦 Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip --root-user-action=ignore \
    && pip install --no-cache-dir -r requirements.txt --root-user-action=ignore \
    && pip install --no-cache-dir -r requirements-ai.txt --root-user-action=ignore \
    && pip install --no-cache-dir uvicorn gunicorn fastapi --root-user-action=ignore

# 📂 Copier le code source complet
COPY src/ /app/src/
COPY scripts/ /app/scripts/
COPY start.sh /app/start.sh
COPY test_import.py /app/test_import.py

# ✅ Vérification institutionnelle de l'import API
RUN python test_import.py || (echo "❌ Échec d'import API" && exit 1)

# 🌐 Exposer le port
EXPOSE 8000

# 🚀 Lancement avec Gunicorn + Uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.apps.api.main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]