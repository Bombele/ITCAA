# ITCAA – Institut Transnational de Certification des Acteurs Armés

![Structure Check](https://github.com/Bombele/ITCAA/actions/workflows/structure-check.yml/badge.svg?branch=main)
![Predeploy Check](https://github.com/Bombele/ITCAA/actions/workflows/structure-check.yml/badge.svg?branch=main&event=push)
![Predeploy Import Check](https://github.com/Bombele/ITCAA/actions/workflows/predeploy_check.yml/badge.svg?branch=main)
![Deploy ITCAA API](https://github.com/Bombele/ITCAA/actions/workflows/deploy.yml/badge.svg?branch=main)
![Annual Report](https://github.com/Bombele/ITCAA/actions/workflows/annual_report.yml/badge.svg)

---

## 🛡️ Conformité technique ITCAA

| Badge | Workflow | Rôle institutionnel |
|-------|----------|----------------------|
| ![Structure Check](https://github.com/Bombele/ITCAA/actions/workflows/structure-check.yml/badge.svg?branch=main) | `structure-check.yml` | Vérifie la cohérence des imports, modules et arborescence |
| ![Predeploy Check](https://github.com/Bombele/ITCAA/actions/workflows/structure-check.yml/badge.svg?branch=main&event=push) | `structure-check.yml` (push) | Bloque le déploiement si `apps` ou `startCommand` sont incorrects |
| ![Predeploy Import Check](https://github.com/Bombele/ITCAA/actions/workflows/predeploy_check.yml/badge.svg?branch=main) | `predeploy_check.yml` | Vérifie automatiquement l’importabilité du module `apps` |
| ![Deploy ITCAA API](https://github.com/Bombele/ITCAA/actions/workflows/deploy.yml/badge.svg?branch=main) | `deploy.yml` | Déploie automatiquement l’API ITCAA sur Render |
| ![Annual Report](https://github.com/Bombele/ITCAA/actions/workflows/annual_report.yml/badge.svg) | `annual_report.yml` | Génère un rapport institutionnel annuel pour mémoire et transparence |

---

## 🎯 Vision
L’ITCAA est une initiative **citoyenne et institutionnelle** fondée par **Camille Bombele Liyama**.  
Elle vise à certifier les acteurs armés non étatiques selon leur conformité au **Droit International Humanitaire (DIH)**, leur **légitimité institutionnelle** et leurs **normes internes**.  
La plateforme combine **IA**, **technologies géospatiales** et **documentation narrative** pour offrir une certification transparente, traçable et évolutive.

---

## 🏗️ Architecture
- **Backend FastAPI** : endpoints pour acteurs, clients, partenaires, risques.  
- **Services Python** : calcul des scores DIH, légitimité, normes internes, typologie.  
- **Base de données SQLAlchemy** : stockage des acteurs, engagements, capsules.  
- **Validation Pydantic** : cohérence et auditabilité des données.  
- **Données YAML/JSON** : dictionnaires de principes et indicateurs, seeds initiaux.  
- **Cartographie GeoJSON + Leaflet/Shapely** : contextualisation géographique.  
- **Interfaces Jinja2 + JS léger** : SSR pour stabilité, interactivité minimale (cartes, filtres, langue).  
- **Démo (`apps/demo/`)** : application illustrative avec composants réutilisables.  

👉 Voir [ARCHITECTURE.md](ARCHITECTURE.md) pour plus de détails.

---

## ⚖️ Protocoles de Certification
1. **DIH** : distinction, proportionnalité, nécessité, humanité.  
2. **Légitimité** : reconnaissance communautaire, non-discrimination, responsabilité interne, traçabilité.  
3. **Normes internes** : codes de conduite, chartes communautaires, engagements humanitaires.  
4. **Géospatial** : localisation des acteurs dans pays/régions sensibles.  

👉 Voir [CERTIFICATION_PROTOCOL.md](CERTIFICATION_PROTOCOL.md).

---

## 🌍 Éthique et DIH
- Les acteurs sont à la fois **sujets du DIH** et **créateurs de normes internes**.  
- L’IA croise engagements documentés et principes normatifs.  
- Les nouvelles technologies assurent transparence et traçabilité.  

👉 Voir [ETHICS_AND_DIH.md](ETHICS_AND_DIH.md).

---

## 🚀 Déploiement
- **Local** : Uvicorn + FastAPI  
- **Docker** : conteneurisation pour portabilité  
- **Cloud** : Render, Hugging Face Spaces, Railway  
- **CI/CD** : GitHub Actions pour tests et déploiement automatisés  

👉 Voir [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 🖥️ Interfaces
### Interface institutionnelle
- SSR avec Jinja2 + JS léger  
- Cartographie interactive (Leaflet + GeoJSON)  
- Rapports multilingues (PDF, HTML)  
- Gouvernance : conseil, alliances, rapports consultatifs  
- LexCivic : soumission citoyenne + certification  

### Interface interactive
- Mode hors-ligne : cache GeoJSON par région  
- Recherche avancée côté client : filtrage instantané, tri par score ou alphabétique  
- UX améliorée sans frameworks lourds  

### Interface citoyenne
- Multilinguisme stratégique : fichiers `data/i18n/{en,fr,es,ar,ru,zh}.json`  
- Sélecteur global de langue  
- Accessibilité : contraste, focus visible, navigation simple  
- Sécurité : RBAC, audit middleware, segmentation des données sensibles  

---

## 🧑‍💻 Développeur principal
- **Camille Bombele Liyama**  
  - Fondateur et architecte institutionnel  
  - Développeur principal (FastAPI, SQLAlchemy, CI/CD, multilinguisme, i18n)

---

## 📜 Mémoire institutionnelle
Chaque jalon technique est documenté comme acte de mémoire et d’empowerment citoyen :  
- Fusion et harmonisation des README multilingues.  
- Validation automatique des imports et modules via CI/CD.  
- Déploiement Render avec healthcheck institutionnel.  
- Intégration des schemas Pydantic pour auditabilité.  
- Publication annuelle via workflow `annual_report.yml`.  
- Roadmap technique consolidée pour partenaires et ONG.  

---

## 🗺️ Roadmap technique ITCAA

| Horizon | Jalons techniques | Objectifs institutionnels |
|---------|------------------|---------------------------|
| 📅 Court terme (0–6 mois) | - Stabilisation du backend FastAPI<br>- Validation automatique avec Pydantic<br>- CI/CD complet (Structure, Predeploy, Deploy)<br>- Documentation multilingue | Transparence technique et auditabilité immédiate |
| 📅 Moyen terme (6–18 mois) | - Module de comptabilité institutionnelle<br>- Intégration des données démographiques<br>- Cartographie interactive GeoJSON<br>- Rapports automatiques annuels | Suivi citoyen et impact démographique |
| 📅 Long terme (18–36 mois) | - Système de scoring DIH/légitimité/normes internes<br>- API ouverte pour ONG et chercheurs<br>- Rapports multilingues (PDF, HTML)<br>- Reconnaissance internationale | Certification citoyenne reconnue et légitimité mondiale |

![🌐 Multilingual Ready](https://github.com/<TON_ORG>/<TON_REPO>/actions/workflows/multilingue.yml/badge.svg)

![🗂 Weekly Index Rebuild](https://github.com/<TON_ORG>/<TON_REPO>/actions/workflows/weekly_rebuild.yml/badge.svg)

📘 README – ITCAA AI

🚀 Installation

Développement
Pour préparer un environnement de développement complet :

`bash
make setup-dev
`

Cette commande installe :
- requirements.txt (dépendances applicatives)
- requirements-dev.txt (outils de développement : lint, tests, mypy…)
- requirements-ai.txt (dépendances IA : torch, transformers, sentence-transformers, faiss, scikit-learn)

👉 Commentaire modification 2025-12-10 : ajout explicite de requirements-ai.txt dans la séquence dev pour alignement avec prod et CI/CD.

---

Production
Pour préparer un environnement de production :

`bash
make setup-prod
`

Cette commande installe :
- requirements.txt (dépendances applicatives)
- requirements-ai.txt (dépendances IA critiques)

👉 Commentaire modification 2025-12-10 : suppression duplication install-prod, correction chemin src/itcaaaioffline/requirements-ai.txt, ordre corrigé dans setup-prod.

---

CI/CD
Les workflows GitHub Actions reflètent exactement ces séquences :

- CI (dev jobs : lint, tests, audit)  
  `yaml
  - name: 📦 Installer les dépendances (Dev)
    run: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      pip install -r requirements-dev.txt
      pip install -r src/itcaaaioffline/requirements-ai.txt
  `

- Deploy / Offline AI / Deploy Render (prod jobs)  
  `yaml
  - name: 📦 Installer les dépendances (Prod)
    run: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      pip install -r src/itcaaaioffline/requirements-ai.txt
  `

👉 Commentaire modification 2025-12-10 : factorisation via _install.yml, suppression des doublons, alignement dev/prod.

---

🧪 Qualité et audit IA

- Lint : black, isort
- Typecheck : mypy
- Tests : pytest
- Audit IA : validate-ai (vérifie dépendances IA et cohérence projet)
- Index FAISS : repair-index et index-builder

👉 Commentaire modification 2025-12-10 : audit IA déplacé après installation des dépendances IA pour éviter les erreurs.

---

📜 Traçabilité (Bitácora)

- 2025-12-10  
  - Suppression duplication install-prod  
  - Correction chemin requirements-ai.txt  
  - Révision séquence setup-prod (ordre corrigé)  
  - Alignement dev/prod/CI-CD  
  - Factorisation workflows via _install.yml

---

🎯 Résultat attendu
- Dev, Prod et CI/CD parfaitement alignés.  
- Audit IA passe ✅ partout.  
- Documentation et traçabilité mises à jour dans README, QUALITY_GUIDE, Bitácora, CI guide, Deploy guide, Dev guide, Readme AI.  

# ITCAA – AI Offline Module

## 🚀 Installation

Toutes les dépendances sont centralisées dans le **Makefile**.  
Avant toute installation, il faut régénérer les fichiers `requirements.txt`, `requirements-dev.txt` et `models/requirements-ai.txt` depuis `poetry.lock`.

### 1. Export des requirements figés
```bash
make export-reqs