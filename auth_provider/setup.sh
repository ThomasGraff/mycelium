#!/bin/sh

set -e

# Variables
AUTHENTIK_URL="http://${AUTHENTIK_HOST:-0.0.0.0}:${AUTHENTIK_PORT:-9000}"

# Source admin credentials
if [ ! -f .admin_creds.tmp ]; then
    echo "❌ Admin credentials file not found. Please run bootstrap.sh first."
    exit 1
fi

source .admin_creds.tmp

# Log in to retrieve an API token
echo "💡 Fetching API token for the admin user..."
AUTHENTIK_TOKEN=$(curl -sSf -X POST "$AUTHENTIK_URL/api/v3/token/auth/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "'"$ADMIN_USERNAME"'",
        "password": "'"$ADMIN_PASSWORD"'"
    }' | jq -r '.token')

echo "✅ Admin API token retrieved."

# Create OAuth application
echo "💡 Creating OAuth application..."
CLIENT_ID=$(openssl rand -hex 16)
CLIENT_SECRET=$(openssl rand -hex 32)

curl -sSf -X POST "$AUTHENTIK_URL/api/v3/oauth2/application/" \
    -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Mycelium OAuth",
        "client_id": "'"$CLIENT_ID"'",
        "client_secret": "'"$CLIENT_SECRET"'",
        "authorization_grant_type": "authorization-code",
        "redirect_uris": ["http://${FRONTEND_HOST:-0.0.0.0}:${FRONTEND_PORT:-80}/callback"],
        "enabled": true
    }'

# Clean up temporary admin credentials
rm .admin_creds.tmp

echo "✅ Setup complete! Client ID: $CLIENT_ID Client Secret: $CLIENT_SECRET"
