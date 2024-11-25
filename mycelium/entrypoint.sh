#!/bin/sh

set -e

# Replace environment variables in the Nginx config
envsubst '$BACKEND_HOST $BACKEND_PORT $FRONTEND_PORT $FRONTEND_HOST' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Verify nginx configuration
nginx -t

# Log the substitution process
echo "🔧 Nginx configuration updated with backend"
echo "🌐 Frontend URL (inside container): http://localhost:${FRONTEND_PORT}"

# Start Nginx with configured logging
exec nginx -g "daemon off;"
