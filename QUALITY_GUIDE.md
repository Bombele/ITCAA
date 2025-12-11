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


📑 Section Audit IA – Appel make validate-ai

`markdown

🔍 Audit IA – Appel du script validate-ai / AI Audit – validate-ai call

📦 Commande / Command

`bash
make validate-ai
`

Cette commande exécute le script scripts/validateaidependencies.py et vérifie la présence des librairies IA critiques.  
This command runs the script scripts/validateaidependencies.py and checks for critical AI libraries.

---

✅ Exemple d’exécution réussie / Example of successful execution

`bash
$ make validate-ai
✅ torch importé avec succès
✅ transformers importé avec succès
✅ sentence-transformers importé avec succès
✅ faiss importé avec succès
✅ scikit-learn importé avec succès

✅ Audit IA réussi : toutes les dépendances sont présentes
`

---

❌ Exemple d’échec / Example of failure

`bash
$ make validate-ai
❌ torch manquant
❌ faiss manquant

❌ Audit IA échoué : dépendances manquantes → torch, faiss
make: * [Makefile:53: validate-ai] Error 1
`

---

🎯 Objectifs institutionnels / Institutional objectives
- Robustesse / Robustness : CI/CD échoue immédiatement si une librairie IA est absente.  
- Traçabilité / Traceability : messages explicites pour chaque dépendance manquante.  
- Transmission / Knowledge transfer : onboarding facilité pour tout contributeur, quelle que soit sa langue. 

 
🧭 QUALITY_GUIDE – ITCAA AI

🎯 Objectif
Garantir la robustesse, la traçabilité et la reproductibilité des environnements Dev, Prod et CI/CD.  
Chaque correction technique est documentée et alignée avec le Makefile et les workflows GitHub Actions.

---

⚙️ Séquences d’installation

| Contexte | Dépendances installées | Commande Makefile | Workflow CI/CD |
|----------|------------------------|-------------------|----------------|
| Dev | requirements.txt + requirements-dev.txt + requirements-ai.txt | make setup-dev | ci.yml (jobs lint, tests, audit) |
| Prod | requirements.txt + requirements-ai.txt | make setup-prod | deploy.yml, offline-ai.yml, deploy_render.yml |
| CI/CD | Reflète exactement Dev ou Prod selon le job | install.yml (paramètre environment) | Tous workflows appellent install.yml |

👉 Commentaire modification 2025-12-10 : alignement complet Dev/Prod/CI-CD, suppression duplication install-prod, correction chemin requirements-ai.txt.

---

🔍 Vérifications qualité

1. Linting  
   - Outils : black, isort  
   - Commande : make lint  
   - CI/CD : étape obligatoire dans ci.yml et predeploy_check.yml.

2. Typecheck  
   - Outil : mypy  
   - Commande : make typecheck  
   - CI/CD : étape obligatoire dans ci.yml.

3. Tests unitaires et intégration  
   - Outil : pytest  
   - Commande : make test  
   - CI/CD : étape obligatoire dans ci.yml, offline-ai.yml.

4. Audit IA  
   - Script : validate-ai  
   - Commande : make validate-ai  
   - CI/CD : étape obligatoire dans ci.yml, offline-ai.yml.

5. Index FAISS  
   - Commandes : make repair-index, make index-builder  
   - CI/CD : exécuté dans jobs IA (offline-ai).

---

📜 Traçabilité (Bitácora)

- 2025-12-10  
  - Suppression duplication install-prod  
  - Correction chemin requirements-ai.txt  
  - Révision séquence setup-prod (ordre corrigé)  
  - Alignement Dev/Prod/CI-CD  
  - Factorisation workflows via _install.yml

---

🎯 Résultat attendu
- Dev → environnement complet pour développement et audit.  
- Prod → environnement minimal mais robuste pour déploiement.  
- CI/CD → reflète exactement ces séquences, sans divergence.  
- Documentation → chaque correction est tracée dans README, QUALITY_GUIDE, Bitácora, CI guide, Deploy guide, Dev guide, Readme AI.  

Mise à jour QUALITY_GUIDE – ITCAA AI

🔍 Objectif
Garantir que toutes les vérifications qualité utilisent des dépendances figées via poetry.lock, pour éviter les divergences et instabilités.

---

⚙️ Vérifications qualité avec requirements figés

- Linting  
  - Outils : black, isort  
  - Dépendances figées dans requirements-dev.txt  
  - Commande CI/CD :  
    `bash
    pip install -r requirements-dev.txt
    make lint
    `

- Typecheck  
  - Outil : mypy  
  - Dépendances figées dans requirements-dev.txt  
  - Commande CI/CD :  
    `bash
    pip install -r requirements-dev.txt
    make typecheck
    `

- Tests unitaires et intégration  
  - Outil : pytest  
  - Dépendances figées dans requirements-dev.txt  
  - Commande CI/CD :  
    `bash
    pip install -r requirements-dev.txt
    make test
    `

- Audit IA  
  - Outils : validate-ai, repair-index, index-builder  
  - Dépendances figées dans requirements-ai.txt (généré depuis poetry.lock)  
  - Commande CI/CD :  
    `bash
    pip install -r src/itcaaaioffline/requirements-ai.txt
    make validate-ai
    `

---

📜 Traçabilité (Bitácora)
- 2025-12-10  
  - Ajout de la règle : toutes les vérifications qualité doivent utiliser les requirements figés (requirements-dev.txt, requirements-ai.txt).  
  - Commit : docs(quality-guide): enforce locked requirements for quality checks

---

🎯 Résultat attendu
- Les institutions disposent d’une garantie de reproductibilité pour les audits qualité.  
- Les programmeurs exécutent lint, typecheck, tests et audit IA avec des dépendances figées → stabilité et cohérence assurées.  


