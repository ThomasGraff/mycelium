#!/bin/sh

# Replace environment variables in the Nginx config
envsubst '$BACKEND_URL' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Print the final Nginx configuration for debugging
echo "🔍 Final Nginx configuration:"
cat /etc/nginx/nginx.conf

# Set log level based on environment variable, default to 'error'
LOG_LEVEL=${NGINX_LOG_LEVEL:-error}

# Start Nginx with configured logging
echo "🚀 Starting Nginx with ${LOG_LEVEL} logging..."
exec nginx -g "daemon off; error_log /dev/stdout ${LOG_LEVEL};"
