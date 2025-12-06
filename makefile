# 📁 Makefile institutionnel pour ITCAA

PYTHONPATH=src
TEST_DIR=tests
SCRIPT_DIR=scripts
INDEX_REPORT=$(PYTHONPATH)/itcaa_ai_offline/data/index/index_report.md
DOCKER_IMAGE=itcaa-ai-api
DOCKER_CONTAINER=itcaa-ai-api

.PHONY: check test index audit clean lint typecheck docker-build docker-up docker-down docker-logs docker-test docker-health

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
	black --check $(PYTHONPATH) $(TEST_DIR) || (echo "❌ Black a trouvé des erreurs" && exit 1)
	isort --check-only $(PYTHONPATH) $(TEST_DIR) || (echo "❌ Isort a trouvé des erreurs" && exit 1)

## 🔎 Vérification stricte des types
typecheck:
	@echo "🔎 Vérification des types avec mypy…"
	PYTHONPATH=$(PYTHONPATH) mypy --config-file=mypy.ini $(PYTHONPATH) $(TEST_DIR) || (echo "❌ Mypy a trouvé des erreurs" && exit 1)

## 🧹 Nettoie les artefacts temporaires
clean:
	@echo "🧹 Nettoyage des fichiers temporaires…"
	rm -rf .pytest_cache __pycache__ */__pycache__ *.pyc *.pyo *.pyd *.log htmlcov/ coverage.xml

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
	@echo "❤️ Vérification de l’endpoint /health…"
	@for i in 1 2 3 4 5; do \
		if curl -s http://localhost:8000/health | grep -q "ok"; then \
			echo "✅ API opérationnelle"; \
			exit 0; \
		fi; \
		echo "⏳ Attente du démarrage de l’API…"; \
		sleep 5; \
	done; \
	echo "❌ API non disponible après 25s"; \
	exit 1

requirements:
	@echo "📦 Export des requirements depuis pyproject.toml…"
	poetry export -f requirements.txt --without-hashes -o requirements.txt
	poetry export -f requirements.txt --without-hashes --with dev -o requirements-dev.txt