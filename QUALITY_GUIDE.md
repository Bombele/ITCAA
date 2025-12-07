🧪 Guide de validation qualité ITCAA

Ce guide explique le cycle qualité institutionnalisé dans le Makefile ITCAA, afin que chaque contributeur puisse garantir la robustesse et la cohérence du code avant tout commit ou déploiement.

🚀 Cycle qualité complet

Le cycle qualité est regroupé dans la cible quality-check et inclut :

Linting (make lint)

Vérifie la conformité du code avec Black et Isort.

Garantit un style homogène et lisible.

Typage (make typecheck)

Vérifie la cohérence des types avec Mypy.

Détecte les erreurs de typage et renforce la robustesse.

Tests (make check-tests)

Lance les tests unitaires et d’intégration avec Pytest.

Génère des rapports de couverture et des logs.

Import (make check-import)

Vérifie que le module apps.api.main est correctement importable.

Assure la validité de la structure du projet.

Dépendances (make validate-deps)

Vérifie la cohérence des dépendances avec pip check et pipdeptree.

Détecte les conflits ou incohérences dans l’environnement Python.

🔒 Pré-commit

La cible pre-commit appelle automatiquement quality-check.Elle garantit que chaque commit est validé par le cycle qualité complet.

Exemple d’utilisation

# Vérification complète de la qualité
make quality-check

# Vérification pré-commit (automatique si hook configuré)
make pre-commit

📂 Bonnes pratiques institutionnelles

Toujours exécuter make quality-check avant un commit ou un déploiement.

Configurer un hook Git (.git/hooks/pre-commit) pour lancer make pre-commit automatiquement.

Consulter les logs générés dans le dossier logs/ pour analyser les résultats détaillés.

Corriger immédiatement toute erreur détectée par lint, typage, tests ou dépendances.

✅ Impact institutionnel

Ce cycle qualité garantit :

Une robustesse technique accrue.

Une traçabilité complète grâce aux logs.

Une cohérence institutionnelle entre développement, CI/CD et production.

Une responsabilisation collective des contributeurs.

En suivant ce guide, chaque contributeur participe à l’amélioration continue et à la consolidation institutionnelle du projet ITCAA.