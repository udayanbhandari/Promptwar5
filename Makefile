PYTHON := python
BACKEND_DIR := backend
FRONTEND_DIR := frontend

.PHONY: lint format typecheck test coverage check backend-lint frontend-lint backend-typecheck frontend-typecheck backend-test frontend-test

backend-lint:
	cd $(BACKEND_DIR) && $(PYTHON) -m ruff check app tests

backend-format:
	cd $(BACKEND_DIR) && $(PYTHON) -m ruff format app tests

backend-typecheck:
	cd $(BACKEND_DIR) && $(PYTHON) -m mypy app

backend-test:
	cd $(BACKEND_DIR) && $(PYTHON) -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90

frontend-lint:
	cd $(FRONTEND_DIR) && npm run lint

frontend-format:
	cd $(FRONTEND_DIR) && npm run format

frontend-typecheck:
	cd $(FRONTEND_DIR) && npm run typecheck

frontend-test:
	cd $(FRONTEND_DIR) && npm test -- --coverage --run

lint: backend-lint frontend-lint
format: backend-format frontend-format
typecheck: backend-typecheck frontend-typecheck
test: backend-test frontend-test
coverage: backend-test frontend-test
check: lint typecheck test
