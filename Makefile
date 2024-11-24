# Load environment variables at the start of each target that needs them
define load_env
	$(eval include $(PWD)/.env)
	$(eval export)
endef

.PHONY: help setup setup-env install-deps launch front back auth

help: ## Show this help message
	@echo '🔍 Usage:'
	@echo '  make <command>'
	@echo ''
	@echo '🎯 Available commands:'
	@echo '  setup        - Install dependencies and create .env file'
	@echo '  setup-env    - Create .env file from example'
	@echo '  install-deps - Install required dependencies'
	@echo '  launch       - Start the application'
	@echo '  front        - Start the frontend application'
	@echo '  back         - Start the backend application'
	@echo '  auth         - Launch the auth_provider application'

install-deps: ## Install required dependencies
	@chmod +x ./scripts/install_deps.sh
	@./scripts/install_deps.sh

setup-env:## Create .env file from example
	@chmod +x ./scripts/setup_env.sh
	@./scripts/setup_env.sh

setup: install-deps setup-env ## Create .env file from example and install dependencies

launch: ## Launch the application
	$(call load_env)
	@chmod +x ./scripts/launch.sh
	@./scripts/launch.sh

front: ## Launch the frontend application
	$(call load_env)
	@cd mycelium && \
	yarn install && \
	yarn cross-env VUE_CLI_SERVICE_CONFIG_PATH=./config/vue.config.js \
	BACKEND_URL=http://${BACKEND_HOST}:${BACKEND_PORT} \
	yarn serve

back: ## Launch the backend application
	$(call load_env)
	@cd backend && \
	poetry install && \
	poetry run uvicorn app.main:app --port ${BACKEND_PORT} --host 0.0.0.0 --reload

	
auth: ## Launch the auth_provider application
	$(call load_env)
	@cd auth_provider && \
	./scripts/launch.sh

