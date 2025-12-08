# 🧱 Étape 1 : Image de base légère pour build
FROM python:3.12-slim AS builder

# 🔧 Variables d’environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# 📦 Installer dépendances système nécessaires (curl, venv, pip)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl python3-venv python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 📦 Installer Poetry via le script officiel
RUN curl -sSL https://install.python-poetry.org | python3 -

# 🔌 Vérifier que Poetry est bien installé
RUN poetry --version

# 🔌 Installer le plugin poetry-plugin-export requis pour `poetry export`
RUN poetry self add poetry-plugin-export

# 📂 Copier uniquement les fichiers de config pour optimiser le cache
COPY pyproject.toml poetry.lock* ./

# 📦 Exporter requirements depuis pyproject.toml
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt \
    && poetry export -f requirements.txt --without-hashes --with dev -o requirements-dev.txt

# 🧱 Étape 2 : Image finale
FROM python:3.12-slim

# 🔧 Variables d’environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=prod \
    PYTHONPATH=/app/src

# 🛠️ Installer dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 📂 Copier requirements exportés
COPY --from=builder /app/requirements.txt /app/requirements.txt
COPY src/itcaa_ai_offline/requirements-ai.txt ./requirements-ai.txt

# 📦 Installer dépendances Python
RUN pip install --no-cache-dir --upgrade pip --root-user-action=ignore \
    && pip install --no-cache-dir -r requirements.txt --root-user-action=ignore \
    && pip install --no-cache-dir -r requirements-ai.txt --root-user-action=ignore \
    && pip install --no-cache-dir uvicorn gunicorn fastapi --root-user-action=ignore

# 📂 Copier le code source
COPY . .

# 🌐 Exposer le port
EXPOSE 8000

# 🚀 Commande de lancement avec Gunicorn + Uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.apps.api.main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]