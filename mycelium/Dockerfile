FROM nginx:alpine

# Set environment variables with default values
ARG BACKEND_HOST
ARG BACKEND_PORT
ARG FRONTEND_HOST
ARG FRONTEND_PORT
ARG NGINX_LOG_LEVEL

ENV BACKEND_HOST=${BACKEND_HOST} \
    BACKEND_PORT=${BACKEND_PORT} \
    FRONTEND_HOST=${FRONTEND_HOST} \
    FRONTEND_PORT=${FRONTEND_PORT} \
    VUE_CLI_SERVICE_CONFIG_PATH=./config/vue.config.js \
    NGINX_LOG_LEVEL=${NGINX_LOG_LEVEL}

# Install node, yarn and curl
RUN apk add --no-cache nodejs npm yarn curl

WORKDIR /app

# Copy files and build frontend
COPY package*.json ./
RUN yarn install
COPY . .
RUN yarn build

# Setup nginx
COPY config/nginx.conf /etc/nginx/nginx.conf.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && \
    mv /app/dist/* /usr/share/nginx/html/ && \
    rm -rf /app

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${FRONTEND_PORT} || exit 1

EXPOSE ${FRONTEND_PORT}

ENTRYPOINT ["/entrypoint.sh"]
