# MODULE_GUIDE.md

_Dernière génération manuelle : 14 décembre 2025_

## 🎯 Objectif du guide
Ce guide documente **tous les modules et fichiers** de la branche `main` du projet ITCAA.  
Il sert de référence pour l’onboarding, la traçabilité et la gouvernance technique.  
Chaque module est détaillé avec ses fichiers internes afin de garantir une **vision claire et factorisée**.

---

## 📂 Modules et fichiers

### `.github/workflows/`
- `annual_report.yml` → Génération automatique du rapport annuel.
- `deploy.yml` → Workflow de déploiement.
- `predeploy.yml` → Vérifications avant déploiement.
- `structure-check.yml` → Validation de la structure du dépôt.

---

### `Bitacora/`
- Journal institutionnel pour la traçabilité.
- Contient les fichiers de suivi des corrections et validations.

---

### `configs/`
- `requirements.txt` → Dépendances principales.
- `requirements-dev.txt` → Dépendances de développement.
- `pyproject.toml` → Configuration du projet Python.

---

### `data/`
- Dictionnaires multilingues pour l’onboarding.
- Seeds pour initialiser les bases de données.

---

### `docs/`
- `ARCHITECTURE_GUIDE.md` → Vue d’ensemble de l’architecture ITCAA.
- `ONBOARDING_BEGINNER.md` → Guide pour débutants.
- `ONBOARDING_INTERMEDIATE.md` → Guide pour contributeurs intermédiaires.
- `ONBOARDING_EXPERT.md` → Guide avancé pour experts.

---

### `econ/`
- Modules économiques et financiers.
- Fichiers de régulation et scoring.

---

### `infra/`
- Scripts et configurations d’infrastructure.
- Gestion des déploiements et conteneurs.

---

### `itcaa_ai_offline/`
- `main.ai.py` → Module IA hors ligne.
- `README-ai.md` → Documentation spécifique IA.
- Intègre FAISS et PyTorch pour recherche sémantique locale.

---

### `models/`
- `pydantic_models.py` → Modèles de validation.
- `sqlalchemy_models.py` → Modèles de base de données.
- Objectif : cohérence et auditabilité des données.

---

### `protocols/`
- Protocoles institutionnels et normatifs.
- Fichiers de certification DIH et conformité.

---

### `scripts/`
- `generate_docs.py` → Génération automatique de `INDEX_GUIDE.md` et `MODULE_GUIDE.md`.
- `auto_update_index.sh` → Script shell pour mise à jour automatique.

---

### `src/`
- `main.py` → Point d’entrée FastAPI.
- Endpoints pour certification et audit.
- Services API institutionnels.

---

### `static/`
- `style.css` → Feuilles de style.
- Ressources front-end.

---

### `templates/`
- `index.html` → Page d’accueil.
- `layout.html` → Template principal.
- Interfaces institutionnelles et citoyennes.

---

### `tests/`
- `test_import.py` → Tests d’intégration.
- Objectif : robustesse et conformité technique.

---

## 📄 Fichiers à la racine
- `README.md` → Présentation générale du projet.
- `INDEX_GUIDE.md` → Sommaire global.
- `MODULE_GUIDE.md` → Ce fichier.
- `LICENSE` → Licence Apache 2.0.
- `render.yaml` → Déploiement Render.
- `start.sh` → Script d’initialisation.
- `check_structure.py` → Vérification de la structure.
- `predeploy_check.py` → Vérifications pré-déploiement.
- `validate_render_config.py` → Validation de configuration Render.

---

## 📌 Synthèse
La branche `main` regroupe :
- **Technique** : backend FastAPI, IA hors ligne, CI/CD complet.  
- **Institutionnelle** : protocoles DIH, Bitacora pour traçabilité.  
- **Documentaire** : guides d’architecture et d’onboarding multilingues.  
- **Front-end** : templates et ressources statiques.  

👉 Ce guide doit être mis à jour automatiquement via CI/CD pour rester fiable et vivant.