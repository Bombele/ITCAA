# 🧠 ARCHITECTURE_GUIDE.md – Visualisation pédagogique du système ITCAA

Ce guide présente l’architecture du projet ITCAA de manière claire, modulaire et pédagogique, pour faciliter l’onboarding technique et institutionnel.

---

## 🔷 1. Backend (FastAPI)
- **Rôle** : Fournit une API institutionnelle pour interagir avec les données, les certifications et les modules IA.
- **Interactions** :
  - Reçoit les requêtes des acteurs (citoyens, institutions).
  - Transmet les données à la base SQLAlchemy.
  - Appelle les modules de vérification et d’indexation.

---

## 🔷 2. Base de données (SQLAlchemy)
- **Rôle** : Stocke toutes les données liées aux certifications, aux acteurs et aux journaux de traçabilité.
- **Interactions** :
  - Enregistre les soumissions d’acteurs.
  - Sert de source pour les audits et les rapports.
  - Alimente les modules IA et les protocoles.

---

## 🔷 3. IA hors ligne (FAISS + PyTorch)
- **Rôle** : Indexe les données et effectue des prédictions supervisées pour certifier les acteurs.
- **Interactions** :
  - Reçoit les données depuis la base.
  - Applique des modèles entraînés pour évaluer la conformité.
  - Retourne un score ou une décision vers le backend.

---

## 🔷 4. Protocoles (DIH, normes internes, légitimité)
- **Rôle** : Définissent les règles de certification et les critères de légitimité.
- **Interactions** :
  - Sont appliqués par le backend pour valider les soumissions.
  - Peuvent être mis à jour par les juristes digitaux.
  - Sont consultés par les institutions pour auditer les décisions.

---

## 🔷 5. Bitácora (journal de traçabilité)
- **Rôle** : Archive chaque correction, validation ou certification avec signature et référence.
- **Interactions** :
  - Reçoit les événements depuis le backend.
  - Génère des rapports via CI/CD.
  - Sert de preuve pour les audits et l’onboarding international.

---

## 🔁 Exemple de flux complet

1. **Acteur** soumet ses données via l’API.
2. **Backend** enregistre dans la base et applique les protocoles.
3. **IA hors ligne** analyse et retourne un score.
4. **Bitácora** documente l’action avec horodatage et référence.
5. **Institution** consulte la Bitácora et délivre la certification.

---

## 📦 Modules techniques

- `src/` : logique applicative (FastAPI, endpoints API, calculs DIH)
- `protocols/` : règles de certification (DIH, normes internes, légitimité institutionnelle)
- `data/` : dictionnaires multilingues, seeds pour initialiser la base
- `bitacora/` : journal de traçabilité (corrections, validations, historique)
- `itcaa_ai_offline/` : module IA hors ligne (index FAISS, prédiction supervisée)

---

## 🧭 Rôles et parcours

- **Développeur** → installe l’environnement, lance API/IA, écrit tests, push → CI valide
- **Juriste digital** → configure `protocols/`, valide DIH, rédige chartes et règles
- **Institution** → lit rapports, déclenche certification, publie décisions dans Bitácora

---

## 🏗️ CI/CD et certification

- `structure-check.yml` → vérifie la structure du projet
- `predeploy_check.yml` → lint, typecheck, tests
- `deploy.yml` → déploiement automatisé
- `annual_report.yml` → génération de rapports institutionnels

**Couches de certification :**
- Protocoles DIH
- Légitimité institutionnelle
- Normes internes

**Audit IA :**
- Lint / Typecheck
- Tests unitaires
- Reproductibilité
- Hors-ligne (FAISS + PyTorch)

---

Ce guide peut être relié dans `INDEX_GUIDE.md` et enrichi par des schémas visuels dans les guides d’onboarding.
