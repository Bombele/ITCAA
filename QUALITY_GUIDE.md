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