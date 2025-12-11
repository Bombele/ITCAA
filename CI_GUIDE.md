# 🛠 Guide CI/CD ITCAA

Ce document explique le fonctionnement du pipeline CI/CD et la lecture des artefacts générés.

---

## 🚀 Déclencheurs du pipeline
Le pipeline CI/CD se lance automatiquement dans les cas suivants :
- **Push sur `main`** : ajout ou modification de corpus (`*.txt`) ou du modèle (`model.pt`).
- **Pull request vers `main`** : validation avant fusion.
- **Planification hebdomadaire** : chaque dimanche à 03h00 UTC.
- **Lancement manuel** : via `workflow_dispatch`.

---

## 📊 Étapes principales
1. **Validation de l’index FAISS**
   - Vérification et réparation (`repair_index.py`).
   - Mise à jour incrémentale si de nouveaux fichiers corpus sont ajoutés.
   - Reconstruction complète hebdomadaire.
   - Tests exécutés :
     - `test_integration_index.py` : cohérence FAISS/meta.json.
     - `test_integration_multilingue.py` : support des langues ONU.
     - `test_index_incremental.py` : ajout incrémental validé.

2. **Validation du modèle**
   - Chargement du modèle (`model_loader.py`).
   - Tests exécutés :
     - `test_model_loader.py` : existence, compatibilité, mode `eval()`, détection CPU/GPU.

3. **Rapport d’index**
   - Génération automatique (`generate_index_report.py`).
   - Contient :
     - Date de dernière reconstruction.
     - Nombre de passages et vecteurs FAISS.
     - Langues détectées.
     - Extraits des premiers passages.

---

## 📂 Artefacts générés
- **`index-report.md`**
  - Rapport sur l’état de l’index FAISS.
  - À partager pour audit institutionnel.
- **`model-loader-test-report`**
  - Résultats des tests sur le modèle PyTorch.
  - Vérifie que le modèle reste chargeable et compatible.

---

## 🔎 Lecture des résultats
- **Succès (`✅`)** : l’index et le modèle sont cohérents et utilisables.
- **Échec (`❌`)** : un test a échoué, consulter les logs pour identifier :
  - Corpus manquant ou corrompu.
  - Index FAISS incohérent.
  - Modèle introuvable ou incompatible.

---

## 📅 Bonnes pratiques
- Vérifier chaque semaine le rapport `index-report.md`.
- En cas d’ajout de corpus, s’assurer que les nouveaux fichiers apparaissent dans `meta.json`.
- En cas de mise à jour du modèle, valider que `test_model_loader.py` passe sans erreur.
- Conserver les artefacts comme preuve d’audit et traçabilité.

---

📘 CI Guide – ITCAA AI (corrigé)

🎯 Objectif
Assurer que les jobs CI/CD utilisent des dépendances figées via poetry.lock, afin d’éviter les versions instables ou trop récentes.

---

⚙️ Séquences d’installation corrigées

Dev jobs (lint, tests, audit)
`yaml
- name: 📦 Installer les dépendances (Dev)
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pip install -r src/itcaaaioffline/requirements-ai.txt
`

👉 Commit : fix(ci): use locked requirements for dev jobs

---

Prod jobs (build, déploiement, offline AI, render)
`yaml
- name: 📦 Installer les dépendances (Prod)
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r src/itcaaaioffline/requirements-ai.txt
`

👉 Commit : fix(ci): use locked requirements for prod jobs

---

🔍 Vérifications qualité en CI
- Lint : black, isort  
- Typecheck : mypy  
- Tests : pytest  
- Audit IA : validate-ai  
- Index FAISS : repair-index, index-builder

👉 Commit : docs(ci-guide): document quality checks with locked deps

---

📜 Traçabilité (Bitácora)
- 2025-12-10  
  - Correction chemin IA (src/itcaaaioffline → src/itcaaaioffline)  
  - Alignement Dev/Prod/CI-CD  
  - Ajout lock file (poetry.lock) pour figer les versions instables  
  - Mise à jour CI Guide pour refléter l’utilisation des requirements figés  
  - Commit : chore(bitacora): log ci guide corrections with lock file

---

🎯 Résultat attendu
- CI/CD utilise toujours les versions figées → reproductibilité garantie.  
- Plus de risque lié aux versions instables (fsspec, regex, certifi).  
- Dev et Prod alignés avec le même lock file.  

