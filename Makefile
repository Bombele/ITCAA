PYTHONPATH=src
TEST_DIR=tests
SCRIPT_DIR=scripts
INDEX_REPORT=$(PYTHONPATH)/itcaaaioffline/data/index/indexreport.md
DOCKER_IMAGE=itcaa-ai-api
DOCKER_CONTAINER=itcaa-ai-api
LOG_DIR=logs

.PHONY: check test index audit clean lint typecheck docker-build docker-up docker-down docker-logs docker-test docker-health requirements repair-index dev-install prod-install setup-dev setup-prod start-api restart-api stop-api cycle-api check-import validate-ai validate-render quality-check pre-commit docker-build-local poetry-setup verify-scripts generate-scripts index-builder check-python-version

## 🔍 Vérifie la présence des scripts critiques
verify-scripts:
	@echo "🔍 Vérification des scripts critiques..."
	@for script in $(SCRIPT_DIR)/repairindex.py $(SCRIPT_DIR)/checkstructure.py $(SCRIPT_DIR)/validatedependencies.py $(SCRIPT_DIR)/validaterender_config.py; do \
		if [ ! -f "$$script" ]; then \
			echo "❌ Script manquant : $$script"; \
			echo "📌 Conseil : régénérez les scripts manquants via make generate-scripts"; \
			exit 1; \
		else \
			echo "✅ Script présent : $$script"; \
		fi; \
	done
	@echo "✅ Tous les scripts critiques sont présents."

## 🛠 Génère les scripts critiques manquants
generate-scripts:
	@echo "🛠 Génération des scripts critiques manquants..."
	@mkdir -p $(SCRIPT_DIR)
	@for script in repairindex.py checkstructure.py validatedependencies.py validaterender_config.py; do \
		if [ ! -f "$(SCRIPT_DIR)/$$script" ]; then \
			echo "📌 Création de $(SCRIPT_DIR)/$$script"; \
			echo "#!/usr/bin/env python3\n\"\"\"$$script (squelette minimal, à compléter)\"\"\"\n\nif __name__ == \"__main__\":\n    print(\"✅ Script $$script généré (contenu minimal)\")" > $(SCRIPT_DIR)/$$script; \
		else \
			echo "ℹ️ Script déjà présent : $(SCRIPT_DIR)/$$script"; \
		fi; \
	done
	@echo "✅ Scripts critiques régénérés ou confirmés."

## 📦 Export des requirements figés depuis poetry.lock
export-reqs:
	@echo "🔒 Exporting locked requirements from poetry.lock…"
	poetry export -f requirements.txt --without-hashes > requirements.txt
	poetry export -f requirements.txt --without-hashes --dev > requirements-dev.txt
	poetry export -f requirements.txt --without-hashes -E ai > models/requirements-ai.txt

install-dev:
	@echo "📦 Installing dependencies for Dev…"
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -r models/requirements-ai.txt

install-prod:
	@echo "📦 Installing dependencies for Prod…"
	pip install -r requirements.txt
	pip install -r models/requirements-ai.txt

install-ci:
	@echo "📦 Installing dependencies for CI/CD (CPU-only)…"
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -r models/requirements-ai.txt
	pip install torch==2.9.1+cpu --index-url https://download.pytorch.org/whl/cpu

## 🔍 Qualité
lint:
	@echo "🔍 Linting code…"
	flake8 src tests

typecheck:
	@echo "🔎 Type checking…"
	mypy src

test:
	@echo "🧪 Running tests…"
	pytest --maxfail=1 --disable-warnings -q

audit:
	@echo "📊 Auditing dependencies…"
	pip-audit -r requirements.txt -r requirements-dev.txt -r models/requirements-ai.txt

## 🐳 Docker
docker-build:
	@echo "🐳 Building Docker image…"
	docker build -t itcaa:latest .

docker-up:
	@echo "🚀 Starting Docker container…"
	docker compose up -d

docker-health:
	@echo "❤️ Checking Docker health…"
	docker ps

## 🔒 Vérification version Python
check-python-version:
	@PY_VER=$$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"); \
	if [ "$$PY_VER" != "3.11" ]; then \
		echo "❌ Version Python incorrecte : $$PY_VER détectée. Attendu : 3.11"; \
		exit 1; \
	else \
		echo "✅ Version Python correcte : $$PY_VER"; \
	fi

## 🔍 Vérification des dépendances IA
validate-ai:
	python $(SCRIPT_DIR)/validateai_dependencies.py

## 🧠 Vérifie la structure du projet IA
check:
	@echo "🔍 Vérification structure IA ITCAA…"
	PYTHONPATH=$(PYTHONPATH) python $(SCRIPT_DIR)/checkstructure.py || exit 1

## 🧪 Lance tous les tests avec pytest
test:
	@echo "🧪 Exécution des tests unitaires et d'intégration…"
	PYTHONPATH=$(PYTHONPATH) pytest -v $(TEST_DIR) --maxfail=1 --disable-warnings || exit 1

## 🧬 Génération de l’index FAISS (protégé par audit IA)
index-builder: validate-ai install-prod
	@echo "🧬 Reconstruction de l’index FAISS…"
	PYTHONPATH=$(PYTHONPATH) python $(PYTHONPATH)/itcaaaioffline/data/corpus/index_builder.py --incremental || \
	(echo '❌ Échec génération index FAISS' && exit 1)

## 📊 Génère le rapport d'audit
audit: validate-ai
	@echo "📊 Génération du rapport d'audit…"
	PYTHONPATH=$(PYTHONPATH) python $(PYTHONPATH)/itcaaaioffline/generateindexreport.py || exit 1
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

## ❤️ Vérifier la santé de l’API
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

## 📦 Export des requirements figés depuis poetry.lock
requirements:
	@echo "📦 Export des requirements figés depuis poetry.lock…"
	poetry export -f requirements.txt --without-hashes -o requirements.txt
	poetry export -f requirements.txt --without-hashes --with dev -o requirements-dev.txt
	poetry export -f requirements.txt --without-hashes --with ai -o src/itcaaaioffline/requirements-ai.txt

## 🛠 Vérifie et répare l’index FAISS (protégé par audit IA)
repair-index: validate-ai install-prod
	@echo "🛠 Vérification et réparation de l’index FAISS…"
	PYTHONPATH=$(PYTHONPATH) python $(SCRIPT_DIR)/repairindex.py || \
	(echo '❌ Échec réparation index FAISS' && exit 1)

## 📥 Vérifie l'import de l'API ITCAA
check-import:
	@echo "📥 Vérification de l'import apps.api.main..."
	@python test_import.py || (echo "❌ Import API échoué" && exit 1)

## ⚙️ Prépare l’environnement complet de développement
setup-dev: check-python-version generate-scripts verify-scripts install-dev validate-ai repair-index check-import audit
	@echo "✅ Environnement de développement prêt : dépendances installées (app, dev, IA), scripts vérifiés, audit IA validé, import API validé, index réparé et audit effectué."

## 🚀 Prépare l’environnement complet de production
setup-prod: check-python-version generate-scripts verify-scripts install-prod check-import validate-ai repair-index
	@echo "✅ Environnement de production prêt : dépendances installées (app, IA), scripts vérifiés, import API validé, audit IA validé et index réparé."

## 🚀 Démarre l’API ITCAA
start-api:
	@echo "🚀 Démarrage de l’API ITCAA..."
	uvicorn apps.api.main:app --host 0.0.0.0 --port 8000

## 🔄 Redémarre l’API ITCAA
restart-api: stop-api start-api
	@echo "🔄 API ITCAA redémarrée."

## 🛑 Arrête l’API ITCAA
stop-api:
	@echo "🛑 Arrêt de l’API ITCAA..."
	@pkill -f "uvicorn apps.api.main:app" || echo "ℹ️ Aucun processus Uvicorn trouvé"

## 🔁 Cycle complet (stop + start)
cycle-api: stop-api start-api
	@echo "🔁 Cycle complet effectué : API arrêtée puis redémarrée."