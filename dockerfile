# Étape 1 : Image de base légère
FROM python:3.11-slim

# Étape 2 : Variables d’environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=prod \
    PYTHONPATH=/app/src

# Étape 3 : Installer dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Étape 4 : Créer répertoire de travail
WORKDIR /app

# Étape 5 : Copier requirements
COPY requirements.txt .
COPY src/itcaa_ai_offline/requirements-ai.txt ./requirements-ai.txt

# Étape 6 : Installer dépendances Python
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install -r requirements-ai.txt \
    && pip install uvicorn gunicorn fastapi

# Étape 7 : Copier le code source
COPY . .

# Étape 8 : Exposer le port
EXPOSE 8000

# Étape 9 : Commande de lancement avec Gunicorn + Uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main.ai:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]