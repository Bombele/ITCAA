# ============================================================
# ITCAA Makefile – version corrigée et extensible
# ============================================================

# -----------------------------
# 🔒 Export des requirements
# -----------------------------
export-reqs:
	@echo "🔒 Exporting locked requirements from poetry.lock…"
	poetry export -f requirements.txt --without-hashes > requirements.txt
	poetry export -f requirements.txt --without-hashes --dev > requirements-dev.txt
	poetry export -f requirements.txt --without-hashes -E ai > models/requirements-ai.txt

# -----------------------------
# 📦 Installation
# -----------------------------
install-dev:
	@echo "📦 Installing dependencies for Dev…"
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -r models/requirements-ai.txt

install-prod:
	@echo "📦 Installing dependencies pour Prod…"
	pip install -r requirements.txt
	pip install -r models/requirements-ai.txt

install-ci:
	@echo "📦 Installing dependencies pour CI/CD (CPU-only)…"
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -r models/requirements-ai.txt
	pip install torch==2.9.1+cpu --index-url https://download.pytorch.org/whl/cpu

# -----------------------------
# 🔎 Vérification Torch
# -----------------------------
check-torch:
	@echo "🔎 Vérification de la version Torch installée…"
	@TORCH_VERSION=$$(pip freeze | grep torch); \
	echo "Torch détecté: $$TORCH_VERSION"; \
	if echo "$$TORCH_VERSION" | grep -q "+cu"; then \
		echo "❌ Torch GPU détecté (CUDA build). Seule la version CPU est autorisée."; \
		exit 1; \
	fi; \
	if ! echo "$$TORCH_VERSION" | grep -q "+cpu"; then \
		echo "❌ Torch CPU-only non détecté. Installez torch==2.9.1+cpu."; \
		exit 1; \
	fi; \
	echo "✅ Torch CPU-only confirmé."

# -----------------------------
# 🧪 Tests et Qualité
# -----------------------------
test:
	pytest --maxfail=1 --disable-warnings -q

lint:
	flake8 src tests

typecheck:
	mypy src

audit:
	pip-audit -r requirements.txt -r requirements-dev.txt -r models/requirements-ai.txt

coverage:
	pytest --cov=src --cov-report=term-missing

# -----------------------------
# 🌐 Tests API (FastAPI)
# -----------------------------
api-test:
	pytest tests/test_capsules_api.py --maxfail=1 --disable-warnings -q

# -----------------------------
# 🔧 CI/CD Helpers
# -----------------------------
ci-install: install-ci
ci-test: test
ci-lint: lint
ci-typecheck: typecheck
ci-audit: audit

ci-all: ci-install ci-lint ci-typecheck ci-test ci-audit api-test

# -----------------------------
# 📚 Documentation
# -----------------------------
docs-build:
	sphinx-build -b html docs build/docs

docs-clean:
	rm -rf build/docs

docs-serve:
	python -m http.server --directory build/docs 8000

# -----------------------------
# 🐳 Docker
# -----------------------------
docker-build:
	docker build -t itcaa:latest .

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-health:
	docker ps

docker-logs:
	docker compose logs -f

# -----------------------------
# 🛠️ DevOps / Maintenance
# -----------------------------
clean-pyc:
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.pyo" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -rf {} +

clean-build:
	rm -rf build dist *.egg-info

reset-env:
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate && make install-dev

# -----------------------------
# 🔍 Git Helpers
# -----------------------------
git-status:
	git status

git-log:
	git log --oneline --graph --decorate --all

git-clean:
	git clean -fd

# -----------------------------
# 🧩 Onboarding
# -----------------------------
onboarding:
	@echo "🚀 Onboarding ITCAA"
	@echo "1. make export-reqs"
	@echo "2. make install-dev"
	@echo "3. make check-torch"
	@echo "4. make test"
	@echo "5. make lint && make typecheck"
	@echo "6. make docs-build"

# -----------------------------
# 🔓 Ajouts progressifs
# -----------------------------
# Tu peux ajouter ici d'autres cibles institutionnelles, modules AI, branches secondaires, etc.