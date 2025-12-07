# 📘 Guide d'utilisation des cibles API ITCAA

Ce guide explique comment utiliser les cibles du **Makefile institutionnel** pour gérer le cycle de vie de l’API ITCAA.

---

## 🚀 Démarrage de l’API

### `make start-api ENV=dev`
- Lance l’API en **mode développement**.
- Active le rechargement automatique (`--reload`) pour faciliter les corrections.

### `make start-api ENV=prod`
- Lance l’API en **mode production**.
- Démarrage optimisé sans rechargement automatique.

---

## 🛑 Arrêt de l’API

### `make stop-api`
- Arrête proprement l’API ITCAA.
- Si aucun processus n’est trouvé, un message informatif est affiché.

---

## 🔄 Redémarrage de l’API

### `make restart-api ENV=dev`
- Arrête puis relance l’API en **mode développement**.

### `make restart-api ENV=prod`
- Arrête puis relance l’API en **mode production**.

---

## 🔄 Cycle complet de l’API

### `make cycle-api ENV=dev`
- Exécute un cycle complet : arrêt puis relance en **mode développement**.

### `make cycle-api ENV=prod`
- Exécute un cycle complet : arrêt puis relance en **mode production**.

---

## 📂 Bonnes pratiques institutionnelles

- Toujours préciser la variable `ENV` (`dev` ou `prod`) pour éviter les ambiguïtés.
- Utiliser `start-api` pour lancer, `stop-api` pour arrêter, `restart-api` pour redémarrer, et `cycle-api` pour un cycle complet.
- En CI/CD et Render, privilégier `setup-prod` suivi de `start-api ENV=prod` pour garantir un environnement cohérent.

---

## 🧾 Exemple d’utilisation

```bash
# Démarrer en mode développement
make start-api ENV=dev

# Arrêter l’API
make stop-api

# Redémarrer en mode production
make restart-api ENV=prod

# Cycle complet en mode développement
make cycle-api ENV=dev