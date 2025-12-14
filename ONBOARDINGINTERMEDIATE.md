### 🧩 ONBOARDING_INTERMEDIATE.md
```markdown
# ONBOARDING – Intermédiaire (Modules clés)

## 🎯 Objectif
Permettre aux contributeurs techniques et institutionnels de comprendre les composants principaux et de commencer à interagir avec eux.

## 🗂 Modules principaux
- **`src/`** : logique applicative (FastAPI, calculs DIH, endpoints API).  
- **`protocols/`** : règles de certification (DIH, légitimité institutionnelle, normes internes).  
- **`data/`** : dictionnaires multilingues, seeds pour initialiser la base.  
- **`bitacora/`** : journal de traçabilité, chaque correction documentée.  
- **`itcaa_ai_offline/`** : module IA hors ligne (index FAISS, prédiction supervisée).  

## 📚 Guides associés
- **`MODULE_GUIDE.md`** : explication détaillée des modules.  
- **`DEV_GUIDE.md`** : installation et configuration de l’environnement de développement.  
- **`DEPLOY_GUIDE.md`** : déploiement local, Docker, cloud.  
- **`QUALITY_GUIDE.md`** : normes de qualité, audit IA, tests.  

## 🛠️ Exemples pratiques
- Lancer le module IA :  
  ```bash
  python -m itcaa_ai_offline.index_builder
