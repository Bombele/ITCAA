# 📁 Makefile institutionnel pour ITCAA

PYTHONPATH=src
TEST_DIR=tests
SCRIPT_DIR=scripts
INDEX_REPORT=$(PYTHONPATH)/itcaa_ai_offline/data/index/index_report.md

.PHONY: check test index audit clean lint

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

## 🎯 Vérifie le linting et le typage
lint:
	@echo "🎯 Vérification linting et typage…"
	black --check $(PYTHONPATH) $(TEST_DIR) || (echo "❌ Black a trouvé des erreurs" && exit 1)
	isort --check-only $(PYTHONPATH) $(TEST_DIR) || (echo "❌ Isort a trouvé des erreurs" && exit 1)
	mypy $(PYTHONPATH) || (echo "❌ Mypy a trouvé des erreurs" && exit 1)

## 🧹 Nettoie les artefacts temporaires
clean:
	@echo "🧹 Nettoyage des fichiers temporaires…"
	rm -rf .pytest_cache __pycache__ */__pycache__ *.pyc *.pyo *.pyd *.log htmlcov/ coverage.xml
