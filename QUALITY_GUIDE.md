# 🧪 Guide de validation qualité ITCAA

Ce guide explique le cycle qualité institutionnalisé dans le **Makefile ITCAA**, afin que chaque contributeur puisse garantir la robustesse et la cohérence du code avant tout commit ou déploiement.

---

## 🚀 Cycle qualité complet

Le cycle qualité est regroupé dans la cible `quality-check` et inclut :

1. **Linting (`make lint`)**  
   - Vérifie la conformité du code avec **Black** et **Isort**.  
   - Garantit un style homogène et lisible.

2. **Typage (`make typecheck`)**  
   - Vérifie la cohérence des types avec **Mypy**.  
   - Détecte les erreurs de typage et renforce la robustesse.

3. **Tests (`make check-tests`)**  
   - Lance les tests unitaires et d’intégration avec **Pytest**.  
   - Génère des rapports de couverture et des logs.

4. **Import (`make check-import`)**  
   - Vérifie que le module `apps.api.main` est correctement importable.  
   - Assure la validité de la structure du projet.

5. **Dépendances (`make validate-deps`)**  
   - Vérifie la cohérence des dépendances avec `pip check` et `pipdeptree`.  
   - Détecte les conflits ou incohérences dans l’environnement Python.

6. **Configuration Render (`make validate-render`)**  
   - Vérifie la présence et la validité du fichier `render.yaml`.  
   - Contrôle la clé `startCommand` et les services définis.  
   - Assure que la configuration est prête pour le déploiement sur Render.  
   - Génère des logs dans `logs/validate_render_config.log`.

---

## 🔒 Pré-commit

La cible `pre-commit` appelle automatiquement `quality-check`.  
Elle garantit que chaque commit est validé par le cycle qualité complet.

### Exemple d’utilisation
```bash
# Vérification complète de la qualité
make quality-check

# Vérification pré-commit (automatique si hook configuré)
make pre-commit