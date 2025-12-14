# Module AI Offline – Guide

🎯 Objectif  
La branche `feature/ai-offline-module` est dédiée au **développement, expérimentation et durcissement des mécanismes d’intelligence artificielle hors‑ligne**.  
Elle permet de tester, valider et améliorer les systèmes IA déconnectés (offline), garantissant robustesse, auditabilité et conformité institutionnelle avant leur intégration officielle dans la branche principale `itcaa/`.

📁 Structure des fichiers  

• `src/`  
  Code source principal du module IA hors‑ligne :  
  ◦ `main.ai.py` → moteur IA offline  
  ◦ `validate_ai_dependencies.py` → vérification des dépendances IA  
  ◦ `repair_index.py` → réparation et cohérence des index FAISS  
  ◦ `predeploy_check.py` → contrôle pré‑déploiement  

• `models/`  
  Modèles IA et dépendances :  
  ◦ `requirements-ai.txt` → dépendances IA (torch, transformers, faiss, scikit-learn)  
  ◦ fichiers de modèles pré‑entraînés et seeds initiaux  

• `configs/`  
  Configuration institutionnelle et technique :  
  ◦ `pyproject.toml`, `mypy.ini` → cohérence et typage  
  ◦ `render.yaml` → configuration déploiement Render  
  ◦ `dockerfile` → conteneurisation pour portabilité  

• `docs/`  
  Documentation multilingue et institutionnelle :  
  ◦ `ARCHITECTURE.md` → architecture technique  
  ◦ `CERTIFICATION_PROTOCOL.md` → protocoles de certification DIH et légitimité  
  ◦ `ETHICS_AND_DIH.md` → éthique et conformité DIH  
  ◦ `DEPLOYMENT.md` → guide de déploiement  
  ◦ `README-ai.md` → documentation spécifique IA offline  

• `bitacora/`  
  Journal de traçabilité institutionnelle :  
  ◦ corrections techniques, alignement dev/prod, factorisation CI/CD  

• `tests/`  
  ◦ `test_import.py` → vérification des imports et dépendances  
  ◦ `test_check.sh` → cohérence des workflows CI/CD  
  ◦ `test_ai.py` → robustesse des modèles IA offline  

🧪 Tests  
• Unitaires : validation des fonctions IA offline, index FAISS, dépendances  
• Intégration : cohérence entre backend FastAPI, modèles IA et configurations  
• Multilingue : vérification des traductions et cohérence des documents (FR/EN/AR/SW/LN)  

🧭 Gouvernance et impact institutionnel  
• Expérimentation contrôlée dans la branche `feature/ai-offline-module`  
• Traçabilité assurée via la Bitácora et workflows CI/CD  
• Fusion dans `itcaa/` après validation  
• Impact : garantit la robustesse, la transparence et l’auditabilité des modules IA offline pour adoption continentale  

✅ Conclusion  
La branche `feature/ai-offline-module` est le **laboratoire technique d’ITCAA pour l’intelligence artificielle hors‑ligne**.  
Elle permet de tester et durcir les moteurs IA, les dépendances et les workflows multilingues avant leur intégration institutionnelle dans la branche principale `itcaa/`.