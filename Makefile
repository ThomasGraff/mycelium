# Load environment variables at the start of each target that needs them
define load_env
	$(eval include $(PWD)/.env)
	$(eval export)
endef

.PHONY: help check check-dev check-prod setup-env auth front-dev back-dev \
        build-front build-back push-front push-back run-front run-back \
        run-front-local run-back-local clean

help: ## Show this help message
	@echo '🔧 Setup & Utils:'
	@echo '  check-dev       - Check development dependencies'
	@echo '  check-prod      - Check production/deployment dependencies'
	@echo '  setup-env       - Create .env file from example'
	@echo '  clean           - Remove all Docker resources (images, containers, volumes) and .env file'
	@echo ''
	@echo '🚀 Running Applications:'
	@echo '  auth            - Launch the auth_provider application (same for dev and prod)'
	@echo '  front           - Run frontend from Docker Hub image'
	@echo '  back            - Run backend from Docker Hub image'
	@echo '  front-local     - Run frontend from local Docker image (requires to have built the image first)'
	@echo '  back-local      - Run backend from local Docker image (requires to have built the image first)'
	@echo '  front-dev       - Start the frontend locally in development mode'
	@echo '  back-dev        - Start the backend locally in development mode'
	@echo ''
	@echo '📦 Docker Operations:'
	@echo '  build-front     - Build frontend Docker image locally'
	@echo '  build-back      - Build backend Docker image locally'
	@echo '  push-front      - Push frontend image to Docker Hub'
	@echo '  push-back       - Push backend image to Docker Hub'


check-dev: ## Check development dependencies
	@chmod +x ./scripts/check_deps.sh
	@./scripts/check_deps.sh dev

check-prod: ## Check production dependencies
	@chmod +x ./scripts/check_deps.sh
	@./scripts/check_deps.sh deploy

setup-env: ## Create .env file from example
	@chmod +x ./scripts/setup_env.sh
	@./scripts/setup_env.sh

auth: ## Launch the auth_provider application
	$(call load_env)
	@cd auth_provider && \
	./scripts/launch.sh
front: ## Run frontend from Docker Hub image
	$(call load_env)
	@echo "💡 Starting frontend container from Docker Hub..."
	@docker run -d \
		--name mycelium-frontend-hub \
		--env-file .env \
		-p ${FRONTEND_PORT}:${FRONTEND_PORT} \
		${DOCKER_USERNAME}/mycelium-frontend:${IMAGE_TAG}
	@echo "✅ Frontend container started on port ${FRONTEND_PORT}"

back: ## Run backend from Docker Hub image
	$(call load_env)
	@echo "💡 Starting backend container from Docker Hub..."
	@docker run -d \
		--name mycelium-backend-hub \
		--env-file .env \
		-p ${BACKEND_PORT}:${BACKEND_PORT} \
		${DOCKER_USERNAME}/mycelium-backend:${IMAGE_TAG}
	@echo "✅ Backend container started on port ${BACKEND_PORT}"

front-local: build-front ## Run frontend from local image
	$(call load_env)
	@echo "💡 Starting frontend container from local image..."
	@docker run -d \
		--name mycelium-frontend-local \
		--env-file .env \
		-p ${FRONTEND_PORT}:${FRONTEND_PORT} \
		mycelium-frontend:local
	@echo "✅ Frontend container started on port ${FRONTEND_PORT}"

back-local: build-back ## Run backend from local image
	$(call load_env)
	@echo "💡 Starting backend container from local image..."
	@docker run -d \
		--name mycelium-backend-local \
		--env-file .env \
		-p ${BACKEND_PORT}:${BACKEND_PORT} \
		mycelium-backend:local
	@echo "✅ Backend container started on port ${BACKEND_PORT}"


front-dev: ## Launch the frontend application
	$(call load_env)
	@cd mycelium && \
	yarn install && \
	yarn cross-env VUE_CLI_SERVICE_CONFIG_PATH=./config/vue.config.js \
	yarn serve

back-dev: ## Launch the backend application
	$(call load_env)
	@cd backend && \
	poetry install && \
	poetry run uvicorn app.main:app --port ${BACKEND_PORT} --host 0.0.0.0 --reload

build-front: ## Build frontend Docker image locally
	$(call load_env)
	@echo "💡 Building frontend image locally..."
	@docker build \
		--build-arg BACKEND_HOST=${BACKEND_HOST} \
		--build-arg BACKEND_PORT=${BACKEND_PORT} \
		--build-arg FRONTEND_HOST=${FRONTEND_HOST} \
		--build-arg FRONTEND_PORT=${FRONTEND_PORT} \
		--build-arg NGINX_LOG_LEVEL=${NGINX_LOG_LEVEL} \
		-t mycelium-frontend:local ./mycelium
	@echo "✅ Frontend image built successfully"

build-back: ## Build backend Docker image locally
	$(call load_env)
	@echo "💡 Building backend image locally..."
	@docker build \
		--build-arg BACKEND_PORT=${BACKEND_PORT} \
		--build-arg AUTHENTIK_HOST=${AUTHENTIK_HOST} \
		--build-arg AUTHENTIK_PORT=${AUTHENTIK_PORT} \
		--build-arg DATABASE_URL=${DATABASE_URL} \
		--build-arg ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES} \
		-t mycelium-backend:local ./backend
	@echo "✅ Backend image built successfully"

push-front: build-front ## Push frontend image to Docker Hub
	$(call load_env)
	@echo "💡 Pushing frontend image to Docker Hub..."
	@docker tag mycelium-frontend:local ${DOCKER_USERNAME}/mycelium-frontend:${IMAGE_TAG}
	@docker push ${DOCKER_USERNAME}/mycelium-frontend:${IMAGE_TAG}
	@docker tag ${DOCKER_USERNAME}/mycelium-frontend:${IMAGE_TAG} mycelium-frontend:local
	@echo "✅ Frontend image pushed successfully"

push-back: build-back ## Push backend image to Docker Hub
	$(call load_env)
	@echo "💡 Pushing backend image to Docker Hub..."
	@docker tag mycelium-backend:local ${DOCKER_USERNAME}/mycelium-backend:${IMAGE_TAG}
	@docker push ${DOCKER_USERNAME}/mycelium-backend:${IMAGE_TAG}
	@docker tag ${DOCKER_USERNAME}/mycelium-backend:${IMAGE_TAG} mycelium-backend:local
	@echo "✅ Backend image pushed successfully"

clean: ## Clean all Docker resources and configuration files
	@echo "💡 Starting cleanup process..."
	
	@echo "\n🗑️  Stopping and removing containers..."
	-docker stop mycelium-frontend-hub mycelium-backend-hub mycelium-frontend-local mycelium-backend-local authentik-server authentik-worker authentik-postgresql authentik-redis 2>/dev/null || true
	-docker rm mycelium-frontend-hub mycelium-backend-hub mycelium-frontend-local mycelium-backend-local authentik-server authentik-worker authentik-postgresql authentik-redis 2>/dev/null || true
	
	@echo "\n🗑️  Removing Docker images..."
	-docker rmi mycelium-frontend:local mycelium-backend:local 2>/dev/null || true
	-docker rmi $$(docker images --filter "reference=*/mycelium-*" -q) 2>/dev/null || true
	
	@echo "\n🗑️  Removing Docker volumes..."
	-docker volume rm authentik-database authentik-redis 2>/dev/null || true
	-docker volume rm $$(docker volume ls -q --filter name=mycelium) 2>/dev/null || true
	
	@echo "\n🗑️  Removing .env file..."
	-rm -f .env
	
	@echo "\n✅ Cleanup completed successfully"

.PHONY: clean


