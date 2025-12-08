# 📁 Makefile institutionnel pour ITCAA

PYTHONPATH=src
TEST_DIR=tests
SCRIPT_DIR=scripts
INDEX_REPORT=$(PYTHONPATH)/itcaa_ai_offline/data/index/index_report.md
DOCKER_IMAGE=itcaa-ai-api
DOCKER_CONTAINER=itcaa-ai-api
LOG_DIR=logs

.PHONY: check test index audit clean lint typecheck docker-build docker-up docker-down docker-logs docker-test docker-health requirements repair-index dev-install prod-install setup-dev setup-prod start-api restart-api stop-api cycle-api check-tests check-import validate-deps validate-render quality-check pre-commit docker-build-local poetry-setup verify-scripts

## 🔍 Vérifie la présence des scripts critiques
verify-scripts:
	@echo "🔍 Vérification des scripts critiques..."
	@for script in $(SCRIPT_DIR)/repair_index.py $(SCRIPT_DIR)/check_structure.py $(SCRIPT_DIR)/validate_dependencies.py $(SCRIPT_DIR)/validate_render_config.py; do \
		if [ ! -f "$$script" ]; then \
			echo "❌ Script manquant : $$script"; \
			exit 1; \
		else \
			echo "✅ Script présent : $$script"; \
		fi; \
	done
	@echo "✅ Tous les scripts critiques sont présents."

## 🧠 Vérifie la structure du projet IA
check:
	@echo "🔍 Vérification structure IA ITCAA…"
	PYTHONPATH=$(PYTHONPATH) python $(SCRIPT_DIR)/check_structure.py || exit 1

## 🧪 Lance tous les tests avec pytest
test:
	@echo "🧪 Exécution des tests unitaires et d'intégration…"
	PYTHONPATH=$(PYTHONPATH) pytest -v $(TEST_DIR) --maxfail=1 --disable-warnings || exit 1

## 🧬 Reconstruit l'index FAISS
index:
	@echo "🧬 Reconstruction de l'index FAISS…"
	PYTHONPATH=$(PYTHONPATH) python $(PYTHONPATH)/itcaa_ai_offline/data/corpus/index_builder.py --incremental || exit 1

## 📊 Génère le rapport d'audit
audit:
	@echo "📊 Génération du rapport d'audit…"
	PYTHONPATH=$(PYTHONPATH) python $(PYTHONPATH)/itcaa_ai_offline/generate_index_report.py || exit 1
	@echo "✅ Rapport disponible : $(INDEX_REPORT)"

## 🎯 Vérifie le linting
lint:
	@echo "🎯 Vérification linting…"
	@mkdir -p $(LOG_DIR)
	black --check $(PYTHONPATH) $(TEST_DIR) | tee $(LOG_DIR)/black.log || (echo "❌ Black a trouvé des erreurs" && exit 1)
	isort --check-only $(PYTHONPATH) $(TEST_DIR) | tee $(LOG_DIR)/isort.log || (echo "❌ Isort a trouvé des erreurs" && exit 1)

## 🔎 Vérification stricte des types
typecheck:
	@echo "🔎 Vérification des types avec mypy…"
	@mkdir -p $(LOG_DIR)
	PYTHONPATH=$(PYTHONPATH) mypy --config-file=mypy.ini $(PYTHONPATH) $(TEST_DIR) | tee $(LOG_DIR)/mypy.log || (echo "❌ Mypy a trouvé des erreurs" && exit 1)

## 🧹 Nettoie les artefacts temporaires
clean:
	@echo "🧹 Nettoyage des fichiers temporaires…"
	rm -rf .pytest_cache __pycache__ */__pycache__ *.pyc *.pyo *.pyd *.log htmlcov/ coverage.xml $(LOG_DIR)

## 🐳 Construire l'image Docker
docker-build:
	@echo "🐳 Construction de l'image Docker…"
	docker build -t $(DOCKER_IMAGE) .

## 🚀 Lancer le conteneur Docker
docker-up:
	@echo "🚀 Lancement du conteneur Docker…"
	docker run -d --name $(DOCKER_CONTAINER) -p 8000:8000 $(DOCKER_IMAGE)

## 🛑 Arrêter et supprimer le conteneur Docker
docker-down:
	@echo "🛑 Arrêt du conteneur Docker…"
	docker rm -f $(DOCKER_CONTAINER) || true

## 📜 Logs du conteneur Docker
docker-logs:
	@echo "📜 Affichage des logs du conteneur…"
	docker logs -f $(DOCKER_CONTAINER)

## 🧪 Exécuter les tests dans le conteneur
docker-test:
	@echo "🧪 Exécution des tests dans le conteneur…"
	docker exec $(DOCKER_CONTAINER) pytest $(TEST_DIR) --maxfail=1 --disable-warnings --cov=$(PYTHONPATH) --cov-report=term-missing

## ❤️ Vérifier la santé de l’API (amélioré)
docker-health:
	@echo "❤️ Vérification du statut du conteneur..."
	@if ! docker inspect -f '{{.State.Running}}' $(DOCKER_CONTAINER) | grep -q true; then \
		echo "❌ Conteneur non démarré"; \
		docker logs $(DOCKER_CONTAINER); \
		exit 1; \
	fi
	@echo "⏳ Vérification de l’endpoint /health…"
	@for i in 1 2 3 4 5; do \
		if curl -s http://localhost:8000/health | grep -q "ok"; then \
			echo "✅ API opérationnelle"; \
			exit 0; \
		fi; \
		echo "⏳ Attente du démarrage de l’API (tentative $$i)…"; \
		sleep 5; \
	done; \
	echo "❌ API non disponible après 25s"; \
	docker logs $(DOCKER_CONTAINER); \
	exit 1

## 📦 Export des requirements depuis pyproject.toml
requirements:
	@echo "📦 Export des requirements depuis pyproject.toml…"
	poetry export -f requirements.txt --without-hashes -o requirements.txt
	poetry export -f requirements.txt --without-hashes --with dev -o requirements-dev.txt

## 🛠 Vérifie et répare l’index FAISS
repair-index:
	@echo "🛠 Vérification et réparation de l’index FAISS…"
	PYTHONPATH=$(PYTHONPATH) python $(SCRIPT_DIR)/repair_index.py || exit 1

## 📦 Installe les dépendances de développement
dev-install:
	@echo "📦 Installation des dépendances de développement..."
	python -m pip install --upgrade pip
	pip install -r requirements-dev.txt

## 📦 Installe les dépendances de production
prod-install:
	@echo "📦 Installation des dépendances de production..."
	python -m pip install --upgrade pip
	pip install -r requirements.txt

## 📥 Vérifie l'import de l'API ITCAA (robuste)
check-import:
	@echo "📥 Vérification de l'import apps.api.main..."
	@python test_import.py || (echo "❌ Import API échoué" && exit 1)

## ⚙️ Prépare l’environnement complet de développement
setup-dev: verify-scripts dev-install repair-index check-import audit
	@echo "✅ Environnement de développement prêt : dépendances installées, scripts vérifiés, import API validé, index réparé et audit effectué."

## 🚀 Prépare l’environnement complet de production
setup-prod: verify-scripts prod-install repair-index check-import
	@echo "✅ Environnement de production prêt : dépendances installées, scripts vérifiés, import API validé et index réparé."

## 🚀 Démarre l’API ITCAA (mode dev ou prod)
start-api:
	@echo "🚀 Démarrage de l’API ITCAA..."
	ENV=$(ENV) bash start.sh

## 🔄 Redémarre l’API ITCAA (arrêt + relance)
restart-api:
	@echo "🛑 Arrêt de l’API ITCAA..."
	@pkill -f "uvicorn apps.api.main:app" || echo "ℹ️ Aucun processus uvicorn trouvé"
	@echo "🚀 Relance de l’API ITCAA..."
	ENV=$(ENV) bash start.sh

## 🛑 Arrête l’API ITCAA
stop-api:
	@echo "🛑 Arrêt de l’API ITCAA..."
	@pkill -f "uvicorn apps.api.main:app" || echo "ℹ️ Aucun processus uvicorn trouvé"

## 🔄 Cycle complet de l’API ITCAA (arrêt + relance)
cycle-api: stop-api start-api
	@echo "🔄 Cycle complet exécuté : API arrêtée puis relancée en mode $(ENV)."

## 🧪 Vérifie les tests avec couverture et logs
check-tests:
	@echo "🧪 Vérification des tests avec couverture..."
	bash test_check.sh

## 📦 Vérifie la cohérence des dépendances Python
validate-deps:
	@echo "📦 Validation des dépendances Python..."
	python validate_dependencies.py

## 🔍 Vérifie la configuration Render (render.yaml + structure src/)
validate-render:
	@echo "🔍 Validation de la configuration Render..."
	python validate_render_config.py

## 🧪 Vérification complète de la qualité (lint + typage + tests + import + deps + render)
quality-check: lint typecheck check-tests check-import validate-deps validate-render
	@echo "✅ Vérification complète de la qualité terminée : linting, typage, tests, import, dépendances et configuration Render validés."

## 🔒 Vérification pré-commit (qualité complète)
pre-commit: quality-check
	@echo "🔒 Vérification pré-commit exécutée : code validé avant commit."

## 🐳 Teste le build Docker localement
docker-build-local:
	@echo "🐳 Test du build Docker local…"
	docker build -t $(DOCKER_IMAGE) .

## 📦 Installe Poetry et plugin export (méthode unique)
poetry-setup:
	@echo "📦 Installation de Poetry et du plugin export…"
	curl -sSL https://install.python-poetry.org | python3 -
	@echo "➕ Ajout de Poetry au PATH"
	@echo "$$HOME/.local/bin" >> $$GITHUB_PATH || true
	poetry self add poetry-plugin-export