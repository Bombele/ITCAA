📖 Guide de développement ITCAA – Makefile institutionnel

Ce document décrit les cibles du Makefile ITCAA et leur usage dans le cycle de développement et de CI/CD.

---

🧠 Vérification de la structure
- Commande : make check  
- Vérifie que la structure du projet IA est conforme (modules et fichiers essentiels).  
- À lancer avant un commit majeur pour s’assurer que l’architecture est intacte.  

---

🧪 Tests unitaires et d’intégration
- Commande : make test  
- Lance les tests avec pytest, arrête à la première erreur et masque les warnings.  
- À utiliser avant push ou merge pour garantir la stabilité.  

---

🧬 Reconstruction de l’index FAISS
- Commande : make index  
- Reconstruit l’index FAISS utilisé par le module IA.  
- À lancer après modification du corpus ou des données.  

---

📊 Rapport d’audit
- Commande : make audit  
- Génère un rapport d’audit sur l’index FAISS.  
- Sortie : src/itcaaaioffline/data/index/index_report.md.  
- Utile pour documenter l’état de l’index et partager avec l’équipe.  

---

🎯 Linting
- Commande : make lint  
- Vérifie le style de code avec black et isort.  
- À lancer avant commit pour garantir un code homogène.  

---

🔎 Vérification des types
- Commande : make typecheck  
- Vérifie les annotations de type avec mypy (config stricte via mypy.ini).  
- À utiliser pour s’assurer que le typage est cohérent et robuste.  

---

🧹 Nettoyage
- Commande : make clean  
- Supprime les fichiers temporaires (pycache, .pytest_cache, .pyc, logs, coverage).  
- À lancer avant un build ou pour repartir sur une base propre.  

---

🐳 Docker – Build
- Commande : make docker-build  
- Construit l’image Docker de l’API FastAPI.  
- À utiliser avant déploiement ou test conteneurisé.  

---

🚀 Docker – Run
- Commande : make docker-up  
- Lance le conteneur Docker sur http://localhost:8000.  
- À utiliser pour tester l’API en local.  

---

🛑 Docker – Stop
- Commande : make docker-down  
- Arrête et supprime le conteneur Docker.  
- À utiliser après les tests ou pour libérer les ressources.  

---

📜 Docker – Logs
- Commande : make docker-logs  
- Affiche les logs du conteneur en direct.  
- Utile pour diagnostiquer un problème.  

---

🧪 Docker – Tests
- Commande : make docker-test  
- Exécute les tests unitaires directement dans le conteneur.  
- À utiliser pour valider que l’image est fonctionnelle.  

---

❤️ Docker – Health Check
- Commande : make docker-health  
- Vérifie l’endpoint /health de l’API avec retries (jusqu’à 25s).  
- À utiliser pour s’assurer que l’API est opérationnelle après lancement.  

---

✅ Bonnes pratiques
- Toujours lancer make lint et make typecheck avant un commit.  
- Utiliser make test pour valider la stabilité.  
- Nettoyer régulièrement avec make clean.  
- Vérifier la santé du conteneur avec make docker-health après make docker-up.  
