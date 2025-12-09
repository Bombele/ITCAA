## 🛠 Règle institutionnelle : Makefile et CI/CD

### 1. Présence obligatoire dans toutes les branches
- Le **Makefile est présent dans toutes les branches actives** (`integration` et `ai-offline`).
- Cela garantit que les pipelines CI/CD peuvent toujours exécuter les cibles critiques sans erreur.

### 2. Cibles obligatoires
- Les cibles `setup-dev` et `setup-prod` sont **obligatoires dans tous les Makefile**, quelle que soit la branche.
- Ces cibles assurent la préparation cohérente des environnements de développement et de production.
- Les scripts critiques (`verify-scripts`, `generate-scripts`, `repair-index`, `install-faiss`) doivent également être présents dans toutes les branches.

### 3. Différenciation par branche
- **Branche `integration`** :  
  - Contient le Makefile complet avec toutes les cibles CI/CD (tests, audit, Docker, linting, typecheck, etc.).  
  - Sert de socle institutionnel pour valider la robustesse et la qualité globale.
- **Branche `ai-offline`** :  
  - Contient un Makefile minimal, mais conserve obligatoirement `setup-dev` et `setup-prod`.  
  - Se concentre sur les routines IA (FAISS, index, audit, structure).  
  - Les cibles Docker et CI/CD avancées peuvent être absentes pour alléger la maintenance.

### 4. Gouvernance et transmission
- Toute modification du Makefile doit être synchronisée entre les branches pour éviter les divergences.  
- Les cibles critiques (`setup-dev`, `setup-prod`) ne peuvent jamais être supprimées.  
- Les contributeurs doivent se référer à cette règle pour garantir la robustesse et éviter les erreurs de pipeline.

### 5. Audit qualité
- Lors de chaque fusion ou mise à jour, un audit doit vérifier que :  
  - Les deux Makefile existent.  
  - Les cibles critiques sont présentes et fonctionnelles.  
  - Les différences entre `integration` et `ai-offline` sont documentées et justifiées.

## 📦 Règle institutionnelle : Gestion des dépendances Python

### 1. Fichiers de référence
- **requirements.txt**  
  - Contient toutes les dépendances **API + IA** nécessaires au runtime et à la production.  
  - Sert de base pour la cible `prod-install` du Makefile.  
  - Inclut FastAPI, SQLAlchemy, Torch, Transformers, Sentence-Transformers, FAISS, etc.

- **requirements-dev.txt**  
  - Contient toutes les dépendances de **requirements.txt** + les dépendances de développement (tests, linting, typage, CI/CD).  
  - Sert de base pour la cible `dev-install` du Makefile.  
  - Inclut Pytest, Coverage, Mypy, Flake8, Black, Isort, Pre-commit.

### 2. Cibles Makefile associées
- `prod-install` → installe uniquement `requirements.txt` (environnement de production).  
- `dev-install` → installe `requirements-dev.txt` (environnement de développement complet).  
- `setup-prod` et `setup-dev` → orchestrent l’installation, la vérification des scripts critiques, FAISS et l’audit.

### 3. Règle de cohérence
- **Obligatoire** : toute dépendance utilisée dans les scripts IA (`repair_index.py`, `index_builder.py`, etc.) doit être présente dans `requirements.txt`.  
- **Institutionnalisé** : aucun script IA ne doit dépendre d’un fichier séparé (`requirements-ai.txt`, `requirements-ml.txt`, etc.).  
- **Documenté** : la fusion des dépendances API et IA est centralisée dans `requirements.txt`.  
- **Audit** : toute dépendance manquante ou dispersée est considérée comme une faille institutionnelle.

### 4. Audit qualité
- Chaque mise à jour de dépendance doit être validée par un audit CI/CD :  
  - Vérification que `requirements.txt` contient toutes les dépendances runtime (API + IA).  
  - Vérification que `requirements-dev.txt` contient toutes les dépendances de développement.  
  - Test automatique :  
    ```yaml
    - name: Check Python dependencies
      run: python -c "import torch, transformers, sentence_transformers, faiss, fastapi"
    ```

### 5. Transmission collective
- Les contributeurs doivent utiliser `make setup-dev` pour préparer leur environnement local.  
- Les déploiements CI/CD doivent utiliser `make setup-prod`.  
- Cette règle garantit robustesse, traçabilité et onboarding international.

## Vérification des dépendances IA – Règle institutionnelle

### Objectif
Garantir que tous les scripts critiques (ex. `repair_index.py`, `index_builder.py`) disposent des dépendances IA nécessaires avant exécution.  
Cette vérification est institutionnalisée dans le **Makefile** via la cible `check-ia-deps`.

### Règle
- **Obligatoire** : tout appel à `setup-prod` ou `setup-dev` passe par `check-ia-deps`.
- **Interdiction** : aucun fichier séparé (`requirements-ai.txt`) ne doit être utilisé.  
- **Centralisation** : toutes les dépendances IA et API doivent être listées dans `requirements.txt` et `requirements-dev.txt`.

### Implémentation dans le Makefile
```makefile
check-ia-deps:
	@python -c "import torch, transformers, sentence_transformers, faiss" || \
	(echo '❌ Dépendances IA manquantes. Vérifiez requirements.txt et relancez l’installation.' && exit 1)

setup-prod: check-ia-deps install-prod repair-index
setup-dev: check-ia-deps install-dev