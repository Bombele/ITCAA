# 🏗️ ONBOARDING – Expert (CI/CD & Certification)

## 🎯 Objectif
Donner aux architectes techniques et responsables institutionnels les outils pour auditer, certifier et déployer l’infrastructure ITCAA.

## ⚙️ CI/CD complet
Le projet intègre des workflows GitHub Actions pour automatiser les vérifications et les déploiements :

- **`structure-check.yml`** : vérifie la structure du projet.  
- **`predeploy_check.yml`** : lint, typecheck, tests avant déploiement.  
- **`deploy.yml`** : déploiement automatisé.  
- **`annual_report.yml`** : génération de rapports institutionnels.

La parité dev/prod est assurée via :
- **Makefile** : tâches reproductibles (build, test, lint, docs).  
- **`_install.yml`** : installation déterministe.  
- **`requirements.txt`** : dépendances verrouillées pour auditabilité.

## 📜 Certification
L’ITCAA repose sur trois couches de certification :

- **Protocoles DIH** : distinction, proportionnalité, humanité.  
- **Légitimité institutionnelle** : responsabilité interne, reconnaissance communautaire.  
- **Normes internes** : codes de conduite, chartes, procédures de sanction.

## 🤖 Audit IA
- Vérification automatique : lint, typecheck, tests.  
- Validation des dépendances IA.  
- Index FAISS et prédiction supervisée pour certification hors ligne.

## 📓 Traçabilité
Chaque correction technique est documentée dans la Bitácora avec signature, motif, référence commit et lien vers les rapports CI/CD.

## 🛠️ Exemples concrets
- Déclencher pipeline CI/CD :  
   ```bash
   git push origin main
