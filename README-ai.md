# 🧠 Module IA hors ligne – ITCAA

## 🇫🇷 Français

Ce module implémente un système d’intelligence artificielle autonome, conçu pour fonctionner hors ligne. Il renforce la souveraineté technique et la résilience institutionnelle du projet ITCAA.

### Fonctionnalités
- Chargement local du modèle (`model.pt`)
- Prédiction via FastAPI (`/predict`)
- Validation Pydantic des entrées/sorties
- CI/CD local via `offline-ai.yml`

### Usage
```bash
uvicorn main_ai:app --reload

# ITCAA – Corpus multilingue et certification IA

![CI Tests](https://github.com/<TON_ORG>/<TON_REPO>/actions/workflows/ci.yml/badge.svg)

🤖 Readme AI – ITCAA

🎯 Objectif
Documenter les dépendances IA critiques utilisées dans ITCAA, leur rôle et leur installation en Dev et Prod.

---

⚙️ Dépendances IA

Liste principale
- torch → moteur de calcul tensoriel, indispensable pour l’entraînement et l’inférence IA.  
- transformers → modèles NLP avancés (BERT, GPT, etc.).  
- sentence-transformers → embeddings sémantiques pour recherche et indexation.  
- faiss → index vectoriel haute performance pour recherche de similarité.  
- scikit-learn → outils de machine learning classiques (classification, clustering, métriques).  

👉 Commit : docs(readme-ai): document core AI dependencies (torch, transformers, faiss, sklearn)

---

🔄 Alignement Dev / Prod

| Contexte | Dépendances IA installées | Commande Makefile |
|----------|---------------------------|-------------------|
| Dev | requirements-ai.txt (torch, transformers, sentence-transformers, faiss, scikit-learn) + requirements.txt + requirements-dev.txt | make setup-dev |
| Prod | requirements-ai.txt (torch, transformers, sentence-transformers, faiss, scikit-learn) + requirements.txt | make setup-prod |

👉 Commit : fix(readme-ai): align dev and prod sequences with Makefile corrections

---

🧪 Vérifications IA

- validate-ai → vérifie la présence et la cohérence des dépendances IA.  
- repair-index → répare l’index FAISS si nécessaire.  
- index-builder → reconstruit l’index FAISS avec corpus IA.  

👉 Commit : docs(readme-ai): add validate-ai and index repair steps

---

📜 Traçabilité (Bitácora)

- 2025-12-10
  - Correction chemin requirements-ai.txt  
  - Alignement Dev/Prod/CI-CD  
  - Documentation mise à jour dans README, QUALITY_GUIDE, CI Guide, Deploy Guide, Dev Guide, Readme AI  

🤖 Readme AI – ITCAA (corrigé)

🎯 Objectif
Garantir que les dépendances IA critiques sont figées via poetry.lock pour assurer stabilité et reproductibilité en Dev et Prod.

---

⚙️ Dépendances IA figées
- torch  
- transformers  
- sentence-transformers  
- faiss-cpu  
- scikit-learn

👉 Ces dépendances sont exportées depuis poetry.lock vers :  
- requirements.txt  
- requirements-dev.txt  
- requirements-ai.txt

---

🔄 Alignement Dev / Prod avec lock file

| Contexte | Fichiers utilisés | Commande Makefile |
|----------|------------------|-------------------|
| Dev | requirements.txt, requirements-dev.txt, requirements-ai.txt | make install-dev |
| Prod | requirements.txt, requirements-ai.txt | make install-prod |

👉 Les fichiers sont générés automatiquement depuis poetry.lock → reproductibilité garantie.

---

📜 Traçabilité (Bitácora)
- 2025-12-10  
  - Ajout règle : dépendances IA figées via poetry.lock.  
  - Mise à jour Readme AI pour refléter l’utilisation des requirements figés.  
  - Commit : docs(readme-ai): enforce locked requirements for ai dependencies

---

🎯 Résultat attendu
- Les institutions disposent d’une documentation claire sur la gestion des dépendances IA figées.  
- Les programmeurs utilisent toujours les mêmes versions en Dev et Prod → stabilité et cohérence assurées.  

