# 🧪 Guide de validation qualité ITCAA

Ce guide explique le cycle qualité institutionnalisé dans le **Makefile ITCAA**, afin que chaque contributeur puisse garantir la robustesse et la cohérence du code avant tout commit ou déploiement.

---

## 🚀 Cycle qualité complet

Le cycle qualité est regroupé dans la cible `quality-check` et inclut :

1. **Linting (`make lint`)**  
   - Vérifie la conformité du code avec **Black** et **Isort**.  
   - Garantit un style homogène et lisible.

2. **Typage (`make typecheck`)**  
   - Vérifie la cohérence des types avec **Mypy**.  
   - Détecte les erreurs de typage et renforce la robustesse.

3. **Tests (`make check-tests`)**  
   - Lance les tests unitaires et d’intégration avec **Pytest**.  
   - Génère des rapports de couverture et des logs.

4. **Import (`make check-import`)**  
   - Vérifie que le module `apps.api.main` est correctement importable.  
   - Assure la validité de la structure du projet.

5. **Dépendances (`make validate-deps`)**  
   - Vérifie la cohérence des dépendances avec `pip check` et `pipdeptree`.  
   - Détecte les conflits ou incohérences dans l’environnement Python.

6. **Configuration Render (`make validate-render`)**  
   - Vérifie la présence et la validité du fichier `render.yaml`.  
   - Contrôle la clé `startCommand` et les services définis.  
   - Assure que la configuration est prête pour le déploiement sur Render.  
   - Génère des logs dans `logs/validate_render_config.log`.

---

## 🔒 Pré-commit

La cible `pre-commit` appelle automatiquement `quality-check`.  
Elle garantit que chaque commit est validé par le cycle qualité complet.

### Exemple d’utilisation
```bash
# Vérification complète de la qualité
make quality-check

# Vérification pré-commit (automatique si hook configuré)
make pre-commit

## 🚀 Déploiement Render

Le déploiement vers Render est institutionnalisé dans le workflow `deploy.yml`, qui contient deux jobs :

1. **Predeploy Validation (`predeploy-check`)**  
   Ce job vérifie que le code est prêt à être déployé :
   - Installation des dépendances via Poetry.
   - Linting (`black`, `isort`) et typage (`mypy`).
   - Tests unitaires avec couverture (`pytest`).
   - Validation de la configuration Render (`validate_render_config.py`).
   - Exécution du cycle qualité complet (`make quality-check`).
   - Archivage des artefacts : logs et rapport de couverture.

2. **Déploiement Render (`deploy-render`)**  
   Ce job est déclenché uniquement si `predeploy-check` réussit :
   - Authentification via `RENDER_API_KEY` et `RENDER_SERVICE_ID`.
   - Déclenchement du déploiement via l’API Render.
   - Affichage du statut et des logs de réponse.
   - Nettoyage des artefacts temporaires.

### Exemple d’exécution manuelle

```bash
# Lancer le workflow manuellement depuis GitHub
make quality-check
make validate-render
# Push vers main ou feature/ai-offline-module déclenche automatiquement le déploiement

# 🔄 Flux CI/CD – ITCAA

```mermaid
flowchart TD
    A[🧹 Purge environnement] --> B[📦 Installer requirements.txt + requirements-dev.txt]
    B --> C[🔍 Audit IA - make validate-ai]
    C --> D[🛠 Repair-index]
    D --> E[🧬 Index-builder]
    E --> F[📊 Audit report]
    F --> G[🧪 Tests & Coverage]
    G --> H[⚙️ Setup-dev]
    G --> I[🚀 Setup-prod]

📑 Section requirements.txt – Version bilingue

`markdown

📦 Fichier requirements.txt / Requirements file

Ce fichier centralise toutes les dépendances nécessaires au projet ITCAA :
- Dépendances applicatives (API, base de données, serveur web, etc.)
- Dépendances IA critiques (machine learning, NLP, indexation FAISS)

This file centralizes all dependencies required for the ITCAA project:
- Application dependencies (API, database, web server, etc.)
- Critical AI dependencies (machine learning, NLP, FAISS indexing)

---

✅ Contenu fusionné / Merged content

`
fastapi==0.115.14
uvicorn==0.32.1
gunicorn==23.0.0
sqlalchemy==2.0.45
psycopg2-binary==2.9.11
pydantic==2.12.5
pydantic-core==2.41.5
starlette==0.46.2
click==8.3.1
anyio==4.12.0
h11==0.16.0
idna==3.11
packaging==25.0
pyyaml==6.0.3
shapely==2.1.2
typing-extensions==4.15.0
typing-inspection==0.4.2
greenlet==3.3.0
torch>=2.2,<3.0
transformers>=4.40,<5.0
sentence-transformers>=2.2,<3.0
scikit-learn>=1.3,<2.0
faiss-cpu>=1.8,<1.14
`

---

🎯 Objectifs institutionnels / Institutional objectives
- Robustesse / Robustness : toutes les dépendances sont installées en une seule commande.  
- Traçabilité / Traceability : CI/CD échoue immédiatement si une librairie IA est absente.  
- Transmission / Knowledge transfer : onboarding facilité pour tout contributeur, quelle que soit sa langue.  
`
