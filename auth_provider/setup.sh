#!/bin/bash

set -e

# Source environment variables from parent directory's .env file
ENV_FILE="../.env"
if [ -f "$ENV_FILE" ]; then
    echo "💡 Loading environment variables from $ENV_FILE"
    export $(cat "$ENV_FILE" | grep -v '^#' | xargs)
else
    echo "❌ Environment file $ENV_FILE not found"
    exit 1
fi

# Variables
AUTHENTIK_URL="http://${AUTHENTIK_HOST:-0.0.0.0}:${AUTHENTIK_PORT:-9000}"
MAX_RETRIES=30
RETRY_INTERVAL=10

# Function to check if Authentik is ready
check_authentik_health() {
    echo "💡 Checking if Authentik is ready on ${AUTHENTIK_URL}..."
    local retry_count=0
    
    while [ $retry_count -lt $MAX_RETRIES ]; do
        if curl -sSf "$AUTHENTIK_URL/api/v3/root/" > /dev/null 2>&1; then
            echo "✅ Authentik is up and running"
            return 0
        fi
        
        echo "⚠️  Authentik is not ready yet. Retrying in ${RETRY_INTERVAL} seconds... (${retry_count}/${MAX_RETRIES})"
        sleep $RETRY_INTERVAL
        retry_count=$((retry_count + 1))
    done
    
    echo "❌ Authentik failed to become ready within the timeout period"
    return 1
}

# Check for required commands
for cmd in curl jq openssl; do
    if ! command -v $cmd >/dev/null 2>&1; then
        echo "❌ Required command '$cmd' is not installed"
        exit 1
    fi
done

# Check for required environment variables
if [ -z "$AUTHENTIK_ADMIN_PASSWORD" ]; then
    echo "❌ AUTHENTIK_ADMIN_PASSWORD is not set in environment"
    exit 1
fi

# Wait for Authentik to be ready
check_authentik_health || exit 1

# Log in to retrieve an API token
echo "💡 Fetching API token for the admin user..."
AUTHENTIK_TOKEN=$(curl -sSf -X POST "$AUTHENTIK_URL/api/v3/token/auth/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "akadmin",
        "password": "'"$AUTHENTIK_ADMIN_PASSWORD"'"
    }' 2>/dev/null | jq -r '.token')

if [ -z "$AUTHENTIK_TOKEN" ] || [ "$AUTHENTIK_TOKEN" = "null" ]; then
    echo "❌ Failed to retrieve admin API token"
    exit 1
fi

echo "✅ Admin API token retrieved"

# Create OAuth application
echo "💡 Creating OAuth application..."
CLIENT_ID=$(openssl rand -hex 16)
CLIENT_SECRET=$(openssl rand -hex 32)

REDIRECT_URI="http://${FRONTEND_HOST:-0.0.0.0}:${FRONTEND_PORT:-80}/callback"

RESPONSE=$(curl -sSf -X POST "$AUTHENTIK_URL/api/v3/oauth2/application/" \
    -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Mycelium OAuth",
        "client_id": "'"$CLIENT_ID"'",
        "client_secret": "'"$CLIENT_SECRET"'",
        "authorization_grant_type": "authorization-code",
        "redirect_uris": ["'"$REDIRECT_URI"'"],
        "enabled": true
    }' 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "❌ Failed to create OAuth application"
    exit 1
fi

# Save credentials to a file for later use
echo "💡 Saving OAuth credentials..."
cat > .oauth_creds.json << EOF
{
    "client_id": "$CLIENT_ID",
    "client_secret": "$CLIENT_SECRET",
    "redirect_uri": "$REDIRECT_URI"
}
EOF

echo "✅ Setup complete!"
echo "📋 OAuth Credentials:"
echo "   Client ID: $CLIENT_ID"
echo "   Client Secret: $CLIENT_SECRET"
echo "   Redirect URI: $REDIRECT_URI"
echo "💡 Credentials have been saved to .oauth_creds.json"
