# Load environment variables at the start of each target that needs them
define load_env
	$(eval include $(PWD)/.env)
	$(eval export)
endef

.PHONY: help setup install-deps launch front back auth

help: ## Show this help message
	@echo '🔍 Usage:'
	@echo '  make <command>'
	@echo ''
	@echo '🎯 Available commands:'
	@echo '  install-deps - Install required dependencies'
	@echo '  setup        - Install dependencies and create .env file'
	@echo '  launch       - Start the application'
	@echo '  front        - Start the frontend application'
	@echo '  back         - Start the backend application'
	@echo '  auth         - Launch the auth_provider application'

install-deps: ## Install required dependencies
	@chmod +x ./scripts/install_deps.sh
	@./scripts/install_deps.sh

setup: install-deps ## Create .env file from example and install dependencies
	@chmod +x ./scripts/setup_env.sh
	@./scripts/setup_env.sh

launch: ## Launch the application
	$(call load_env)
	@chmod +x ./scripts/launch.sh
	@./scripts/launch.sh

front: ## Launch the frontend application
	$(call load_env)
	@cd mycelium && \
	yarn cross-env VUE_CLI_SERVICE_CONFIG_PATH=./config/vue.config.js \
	BACKEND_URL=http://${BACKEND_HOST}:${BACKEND_PORT} \
	yarn serve

back: ## Launch the backend application
	$(call load_env)
	@cd backend && \
	poetry run uvicorn app.main:app --port ${BACKEND_PORT} --host ${BACKEND_HOST}

auth: ## Launch the auth_provider application
	$(call load_env)
	@cd auth_provider && \
	./scripts/launch.sh

