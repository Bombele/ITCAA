# ITCAA – Guide de Déploiement

## 🎯 Objectif
Ce document décrit les étapes nécessaires pour déployer l’application **ITCAA** :
- En environnement local pour le développement.
- En conteneur Docker pour la portabilité.
- Sur des plateformes cloud (Render, Hugging Face Spaces, Railway).

---

## 🏗️ Prérequis

- **Python 3.10+**
- **Poetry** ou **pip** pour la gestion des dépendances
- **FastAPI** et **Uvicorn**
- **SQLAlchemy** pour la base de données
- **Shapely** pour les calculs géospatiaux
- **Docker** (optionnel, pour conteneurisation)
- Accès à une base de données (SQLite par défaut, PostgreSQL recommandé en production)

---

## 🚀 Déploiement local

1. **Cloner le projet**
   ```bash
   git clone https://github.com/itcaa/justice-digital.git
   cd justice-digital
