# Module AI Offline – Guide

🎯 Objectif  
La branche `feature/ai-offline-module` est dédiée au **développement, expérimentation et durcissement des mécanismes d’intelligence artificielle hors‑ligne**.  
Elle permet de tester, valider et améliorer les systèmes IA déconnectés (offline), garantissant robustesse, auditabilité et conformité institutionnelle avant leur intégration officielle dans la branche principale `itcaa/`.

📁 Structure des fichiers  

• Racine de la branche  
  ◦ `main.ai.py` → moteur IA offline  
  ◦ `validate_ai_dependencies.py` → vérification des dépendances IA  
  ◦ `repair_index.py` → réparation et cohérence des index FAISS  
  ◦ `predeploy_check.py` → contrôle pré‑déploiement  
  ◦ `pyproject.toml` → cohérence et typage  
  ◦ `mypy.ini` → vérification statique des types  
  ◦ `render.yaml` → configuration déploiement Render  
  ◦ `dockerfile` → conteneurisation pour portabilité  

• `models/`  
  ◦ `models/requirements-ai.txt` → dépendances IA (torch, transformers, faiss, scikit-learn)  
  ◦ `models/` → fichiers de modèles pré‑entraînés et seeds initiaux  

• `docs/`  
  ◦ `docs/ARCHITECTURE.md` → architecture technique  
  ◦ `docs/CERTIFICATION_PROTOCOL.md` → protocoles de certification DIH  
  ◦ `docs/ETHICS_AND_DIH.md` → éthique et conformité DIH  
  ◦ `docs/DEPLOYMENT.md` → guide de déploiement  
  ◦ `docs/README-ai.md` → documentation spécifique IA offline  

• `bitacora/`  
  ◦ `bitacora/` → corrections techniques, alignement dev/prod, factorisation CI/CD  

• `tests/`  
  ◦ `tests/test_import.py` → vérification des imports et dépendances  
  ◦ `tests/test_check.sh` → cohérence des workflows CI/CD  
  ◦ `tests/test_ai.py` → robustesse des modèles IA offline  

---

📌 Fichiers recommandés à créer  

• `docs/`  
  ◦ `ai_offline_fr.md`, `ai_offline_en.md`, `ai_offline_ar.md`, `ai_offline_sw.md`, `ai_offline_ln.md` → documentation multilingue homogène  
  ◦ `SECURITY_GUIDE.md` → bonnes pratiques de sécurité pour IA offline  
  ◦ `ONBOARDING.md` → guide rapide pour nouveaux contributeurs  

• `tests/`  
  ◦ `tests/test_docs.py` → vérification de la cohérence multilingue des guides  
  ◦ `tests/test_performance.py` → benchmarks des modèles offline  
  ◦ `tests/test_security.py` → validation des règles de sécurité et conformité  

• `scripts/` (nouveau dossier)  
  ◦ `scripts/sync_versions.py` → vérification et synchronisation des versions des dépendances  
  ◦ `scripts/generate_index.py` → génération initiale des index FAISS  
  ◦ `scripts/cleanup.sh` → nettoyage des artefacts et logs  

---

🧪 Tests  
• Unitaires : validation des fonctions IA offline, index FAISS, dépendances  
• Intégration : cohérence entre backend FastAPI, modèles IA et configurations  
• Multilingue : vérification des traductions et cohérence des documents (FR/EN/AR/SW/LN)  

🧭 Gouvernance et impact institutionnel  
• Expérimentation contrôlée dans la branche `feature/ai-offline-module`  
• Traçabilité assurée via la Bitácora et workflows CI/CD  
• Fusion dans `itcaa/` après validation  
• Impact : robustesse, transparence et auditabilité des modules IA offline pour adoption continentale  

✅ Conclusion  
La branche `feature/ai-offline-module` est le **laboratoire technique d’ITCAA pour l’intelligence artificielle hors‑ligne**.  
Elle permet de tester et durcir les moteurs IA, les dépendances et les workflows multilingues avant leur intégration institutionnelle dans la branche principale `itcaa/`.