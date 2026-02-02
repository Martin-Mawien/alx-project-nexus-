.PHONY: help install install-dev migrate makemigrations test coverage lint format clean run shell createsuperuser

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Job Board Backend - Development Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install production dependencies
	@echo "$(BLUE)Installing production dependencies...$(NC)"
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	python manage.py migrate

makemigrations: ## Create new migrations
	@echo "$(BLUE)Creating new migrations...$(NC)"
	python manage.py makemigrations

test: ## Run tests with pytest
	@echo "$(BLUE)Running tests...$(NC)"
	pytest --verbose

test-fast: ## Run tests in parallel
	@echo "$(BLUE)Running tests in parallel...$(NC)"
	pytest -n auto

coverage: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	pytest --cov=apps --cov-report=html --cov-report=term
	@echo "$(GREEN)Coverage report generated in htmlcov/index.html$(NC)"

coverage-open: coverage ## Generate and open coverage report
	@echo "$(BLUE)Opening coverage report...$(NC)"
	@if command -v xdg-open > /dev/null; then \
		xdg-open htmlcov/index.html; \
	elif command -v open > /dev/null; then \
		open htmlcov/index.html; \
	else \
		echo "$(YELLOW)Please open htmlcov/index.html manually$(NC)"; \
	fi

lint: ## Run all linting tools
	@echo "$(BLUE)Running linting tools...$(NC)"
	@echo "$(YELLOW)Running flake8...$(NC)"
	flake8 apps/
	@echo "$(YELLOW)Running black (check only)...$(NC)"
	black apps/ --check
	@echo "$(YELLOW)Running isort (check only)...$(NC)"
	isort apps/ --check-only
	@echo "$(GREEN)All linting checks passed!$(NC)"

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code...$(NC)"
	@echo "$(YELLOW)Running black...$(NC)"
	black apps/
	@echo "$(YELLOW)Running isort...$(NC)"
	isort apps/
	@echo "$(GREEN)Code formatted successfully!$(NC)"

check: lint test ## Run linting and tests

security: ## Run security checks with bandit
	@echo "$(BLUE)Running security checks...$(NC)"
	bandit -r apps/ -f screen

clean: ## Clean up temporary files
	@echo "$(BLUE)Cleaning up...$(NC)"
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '.coverage' -delete
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	@echo "$(GREEN)Cleanup completed!$(NC)"

run: ## Run development server
	@echo "$(BLUE)Starting development server...$(NC)"
	python manage.py runserver

runserver: run ## Alias for run

shell: ## Open Django shell
	@echo "$(BLUE)Opening Django shell...$(NC)"
	python manage.py shell

shell-plus: ## Open Django shell with django-extensions
	@echo "$(BLUE)Opening enhanced Django shell...$(NC)"
	python manage.py shell_plus

createsuperuser: ## Create a superuser
	@echo "$(BLUE)Creating superuser...$(NC)"
	python manage.py createsuperuser

collectstatic: ## Collect static files
	@echo "$(BLUE)Collecting static files...$(NC)"
	python manage.py collectstatic --noinput

seed-data: ## Load seed data into database
	@echo "$(BLUE)Loading seed data...$(NC)"
	python manage.py loaddata initial_roles initial_categories

docker-build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	docker-compose build

docker-up: ## Start Docker containers
	@echo "$(BLUE)Starting Docker containers...$(NC)"
	docker-compose up -d

docker-down: ## Stop Docker containers
	@echo "$(BLUE)Stopping Docker containers...$(NC)"
	docker-compose down

docker-logs: ## View Docker logs
	@echo "$(BLUE)Viewing Docker logs...$(NC)"
	docker-compose logs -f

docker-shell: ## Open shell in web container
	@echo "$(BLUE)Opening shell in web container...$(NC)"
	docker-compose exec web bash

db-backup: ## Backup database
	@echo "$(BLUE)Backing up database...$(NC)"
	@mkdir -p backups
	python manage.py dumpdata --indent 2 > backups/backup_$$(date +%Y%m%d_%H%M%S).json
	@echo "$(GREEN)Database backup created in backups/$(NC)"

db-restore: ## Restore database from backup (use BACKUP=filename)
	@echo "$(BLUE)Restoring database...$(NC)"
	@if [ -z "$(BACKUP)" ]; then \
		echo "$(RED)Error: Please specify BACKUP=filename$(NC)"; \
		exit 1; \
	fi
	python manage.py loaddata $(BACKUP)
	@echo "$(GREEN)Database restored from $(BACKUP)$(NC)"

update-deps: ## Update dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt

freeze: ## Freeze current dependencies
	@echo "$(BLUE)Freezing dependencies...$(NC)"
	pip freeze > requirements.txt

pre-commit: ## Run pre-commit hooks on all files
	@echo "$(BLUE)Running pre-commit hooks...$(NC)"
	pre-commit run --all-files

setup: install-dev migrate ## Initial project setup
	@echo "$(GREEN)Project setup completed!$(NC)"
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Copy .env.example to .env and configure"
	@echo "  2. Run 'make createsuperuser' to create admin user"
	@echo "  3. Run 'make run' to start development server"

.PHONY: all
all: clean format lint test ## Run all checks
