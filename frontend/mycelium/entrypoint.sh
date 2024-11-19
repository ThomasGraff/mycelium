#!/bin/sh

set -e

# Replace environment variables in the Nginx config
envsubst '$BACKEND_URL $AUTHENTIK_URL $FRONTEND_PORT' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Verify nginx configuration
nginx -t

# Log the substitution process
echo "🔧 Nginx configuration updated with backend and authentik URLs"
echo "🔍 Backend URL: ${BACKEND_URL}"
echo "🔑 Authentik URL: ${AUTHENTIK_URL}"
echo "🌐 Frontend URL (inside container): http://localhost:${FRONTEND_PORT}"

# Start Nginx with configured logging
exec nginx -g "daemon off;"
