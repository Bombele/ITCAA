## 🛠 Règle institutionnelle : Makefile et CI/CD

### 1. Branche `integration`
- Le **Makefile complet** est maintenu dans la branche `integration`.
- Il contient toutes les cibles critiques :  
  - `setup-dev` et `setup-prod` (préparation des environnements)  
  - `verify-scripts` et `generate-scripts` (scripts critiques)  
  - `install-faiss` et `repair-index` (robustesse IA)  
  - `check`, `test`, `audit` (qualité et cohérence)  
  - Cibles Docker et CI/CD (`docker-build`, `docker-up`, `docker-health`, etc.)
- Toute modification du pipeline CI/CD doit être validée dans `integration`.

### 2. Branche `ai-offline`
- Le **Makefile est minimal** dans la branche `ai-offline`.  
- Il conserve uniquement les cibles nécessaires au travail sur l’index et la structure IA :  
  - `setup-dev` et `setup-prod` (compatibilité CI/CD)  
  - `install-faiss` et `repair-index` (gestion FAISS)  
  - `check` et `audit` (structure et rapport index)  
- Les cibles Docker, tests API et CI/CD complet sont supprimées pour alléger la maintenance.

### 3. Règle de cohérence
- **Obligatoire** : chaque branche doit contenir au minimum les cibles `setup-dev` et `setup-prod` pour éviter les failles CI/CD.  
- **Institutionnalisé** : le Makefile officiel est celui de `integration`.  
- **Documenté** : `ai-offline` est volontairement allégé pour éviter les dépendances inutiles.

### 4. Transmission collective
- Toute nouvelle cible doit être ajoutée dans `integration` et validée par audit.  
- Si une cible est utile en offline, elle peut être dupliquée dans le Makefile minimal de `ai-offline`.  
- Les contributeurs doivent se référer à cette règle pour éviter les divergences et erreurs de pipeline.