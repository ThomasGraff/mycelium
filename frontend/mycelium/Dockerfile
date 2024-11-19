FROM nginx:alpine

# Build-time arguments with default values
ARG AUTHENTIK_HOST=host.docker.internal
ARG AUTHENTIK_PORT=9000
ARG BACKEND_HOST=host.docker.internal 
ARG BACKEND_PORT=8000
ARG FRONTEND_PORT=80
ARG NGINX_LOG_LEVEL=error

# Set environment variables
ENV AUTHENTIK_URL=http://${AUTHENTIK_HOST}:${AUTHENTIK_PORT} \
    BACKEND_URL=http://${BACKEND_HOST}:${BACKEND_PORT} \
    FRONTEND_PORT=${FRONTEND_PORT} \
    VUE_CLI_SERVICE_CONFIG_PATH=./config/vue.config.js \
    NGINX_LOG_LEVEL=${NGINX_LOG_LEVEL}

# Install node and yarn
RUN apk add --no-cache nodejs npm yarn

WORKDIR /app

# Copy files and build frontend
COPY package*.json ./
RUN yarn install
COPY config ./config
COPY . .
RUN yarn build

# Setup nginx
COPY config/nginx.conf /etc/nginx/nginx.conf.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && \
    mv /app/dist/* /usr/share/nginx/html/ && \
    rm -rf /app

EXPOSE ${FRONTEND_PORT}

ENTRYPOINT ["/entrypoint.sh"]
