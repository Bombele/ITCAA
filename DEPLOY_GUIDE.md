🚀 DEPLOY_GUIDE – Workflow fusionné Deploy to Render

🔑 Configuration des secrets GitHub
Avant de lancer un déploiement, configure deux secrets dans ton repository GitHub :

- RENDERAPIKEY : clé API fournie par Render (dashboard Render).  
- RENDERSERVICEID : identifiant unique du service Render (visible dans l’URL ou paramètres du service).  

Étapes :
1. Aller dans Settings > Secrets and variables > Actions.  
2. Cliquer sur New repository secret.  
3. Ajouter RENDERAPIKEY avec la valeur correspondante.  
4. Ajouter RENDERSERVICEID avec la valeur correspondante.  

---

⚙️ Déclenchement du workflow
Le workflow deploy-render.yml se déclenche automatiquement :
- Lors d’un push sur main ou feature/ai-offline-module.  
- Manuellement via workflow_dispatch (onglet Actions).  

---

🧪 Étapes du pipeline fusionné
1. Checkout du code → récupération du repository.  
2. Setup Python 3.12 → environnement moderne et stable.  
3. Poetry export → génération des fichiers requirements.txt et requirements-dev.txt.  
4. Cache pip → optimisation des installations.  
5. Installation des dépendances → libs de prod et dev.  
6. Vérification installation → affichage des dépendances installées.  
7. Lint & typecheck → vérification du style et du typage (black, isort, mypy).  
8. Tests avec couverture → exécution des tests unitaires et génération du rapport coverage.xml.  
9. Archivage des artefacts → sauvegarde des logs et rapports.  
10. Déploiement Render → déclenchement via API Render avec gestion d’erreurs et clearCache.  
11. Nettoyage final → suppression des fichiers temporaires.  

---

📊 Vérification du déploiement
Après déclenchement, Render crée un nouveau déploiement visible dans le dashboard. Tu peux :
- Consulter les logs Render pour vérifier l’état du déploiement.  
- Vérifier l’endpoint /health pour confirmer que l’API est opérationnelle.  

---

✅ Bonnes pratiques
- Toujours vérifier que les tests passent avant de merger sur main.  
- Surveiller les logs Render pour détecter les erreurs.  
- Mettre à jour régulièrement pyproject.toml et régénérer les requirements.  
- Utiliser workflow_dispatch pour forcer un déploiement manuel si nécessaire.  

🚀 Deploy Guide – ITCAA AI

🎯 Objectif
Décrire la procédure de déploiement en environnement Prod, alignée avec le Makefile et les workflows CI/CD.

---

⚙️ Séquence de déploiement

Étapes principales
1. Préparer l’environnement Prod
   `bash
   make setup-prod
   `
   - Vérifie la version Python (3.11 obligatoire)
   - Génère et vérifie les scripts critiques
   - Installe les dépendances Prod :
     - requirements.txt
     - requirements-ai.txt
   - Vérifie l’import API
   - Valide les dépendances IA
   - Répare l’index FAISS

👉 Commit : fix(deploy-guide): align setup-prod sequence with Makefile corrections

---

2. Construire l’image Docker
   `bash
   make docker-build
   `

👉 Commit : docs(deploy-guide): document docker build step

---

3. Lancer le conteneur
   `bash
   make docker-up
   `

👉 Commit : docs(deploy-guide): add docker-up step for prod

---

4. Vérifier la santé de l’API
   `bash
   make docker-health
   `

👉 Commit : docs(deploy-guide): add health check step

---

5. Arrêter / Redémarrer l’API
   `bash
   make stop-api
   make restart-api
   `

👉 Commit : docs(deploy-guide): add stop/restart cycle for API

---

📜 Traçabilité (Bitácora)

- 2025-12-10
  - Suppression duplication install-prod
  - Correction chemin requirements-ai.txt
  - Révision séquence setup-prod (ordre corrigé)
  - Alignement Dev/Prod/CI-CD
  - Factorisation workflows via _install.yml

