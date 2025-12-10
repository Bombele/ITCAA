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
