#!/bin/sh

set -e

# Replace environment variables in the Nginx config
envsubst '$BACKEND_URL $BACKEND_HOST $FRONTEND_PORT $FRONTEND_HOST' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Verify nginx configuration
nginx -t

# Log the substitution process
echo "🔧 Nginx configuration updated with backend"
echo "🔍 Backend URL: ${BACKEND_URL}"
echo "🌐 Frontend URL (inside container): http://${FRONTEND_HOST}:${FRONTEND_PORT}"

# Start Nginx with configured logging
exec nginx -g "daemon off;"
