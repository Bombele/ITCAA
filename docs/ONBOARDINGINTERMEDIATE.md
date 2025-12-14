# 🧩 ONBOARDING – Intermédiaire (Modules clés)

## 🎯 Objectif
Permettre aux contributeurs techniques et institutionnels de comprendre les composants principaux et de commencer à interagir avec eux.

## 🗂 Modules principaux
L’architecture modulaire du projet ITCAA repose sur des dossiers bien définis :

- **`src/`** : logique applicative (FastAPI, endpoints API, calculs DIH).  
- **`protocols/`** : règles de certification (DIH, légitimité institutionnelle, normes internes).  
- **`data/`** : dictionnaires multilingues, seeds pour initialiser la base.  
- **`bitacora/`** : journal de traçabilité (corrections, validations, historique).  
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
