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
APP_SLUG="mycelium"

# Function to check if Authentik is ready
check_authentik_health() {
    echo "💡 Checking if Authentik is ready on ${AUTHENTIK_URL}..."
    local retry_count=0
    
    while [ $retry_count -lt $MAX_RETRIES ]; do
        if curl -sSf "$AUTHENTIK_URL/-/health/live/" > /dev/null 2>&1; then
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
for cmd in curl jq; do
    if ! command -v $cmd >/dev/null 2>&1; then
        echo "❌ Required command '$cmd' is not installed"
        exit 1
    fi
done

# Check for required environment variables
if [ -z "$AUTHENTIK_ADMIN_TOKEN" ]; then
    echo "❌ AUTHENTIK_ADMIN_TOKEN is not set in environment"
    exit 1
fi

# Wait for Authentik to be ready
check_authentik_health || exit 1

echo "✅ Using bootstrap admin token"

# Check if application exists
echo "💡 Checking if application exists..."
EXISTING_APP_RESPONSE=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/core/applications/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -G --data-urlencode "slug=$APP_SLUG")

APP_UUID=$(echo $EXISTING_APP_RESPONSE | jq -r ".results[] | select(.slug==\"$APP_SLUG\") | .pk")

if [ -z "$APP_UUID" ] || [ "$APP_UUID" = "null" ]; then
    echo "💡 Application does not exist, creating new one..."
    APPLICATION_RESPONSE=$(curl -s -X POST "$AUTHENTIK_URL/api/v3/core/applications/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Mycelium",
            "slug": "'"$APP_SLUG"'",
            "meta_description": "Mycelium Application",
            "meta_publisher": "Mycelium"
        }')

    APP_UUID=$(echo $APPLICATION_RESPONSE | jq -r '.pk')

    if [ -z "$APP_UUID" ] || [ "$APP_UUID" = "null" ]; then
        echo "❌ Failed to create Application"
        echo "$APPLICATION_RESPONSE"
        exit 1
    fi
    echo "✅ Application created with UUID: $APP_UUID"
else
    echo "✅ Found existing application with UUID: $APP_UUID"
fi

# Check if OAuth2 provider exists for this application
echo "💡 Checking if OAuth2 provider exists..."
EXISTING_PROVIDER_RESPONSE=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/providers/oauth2/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json")

# First try to find provider by application
PROVIDER_ID=$(echo $EXISTING_PROVIDER_RESPONSE | jq -r ".results[] | select(.application==\"$APP_UUID\") | .pk")

# If not found by application, try by name
if [ -z "$PROVIDER_ID" ] || [ "$PROVIDER_ID" = "null" ]; then
    PROVIDER_ID=$(echo $EXISTING_PROVIDER_RESPONSE | jq -r '.results[] | select(.name=="Mycelium OAuth Provider") | .pk')
fi

if [ -z "$PROVIDER_ID" ] || [ "$PROVIDER_ID" = "null" ]; then
    echo "💡 No existing provider found, creating new one..."
    echo "💡 Getting default authorization flow UUID..."
    FLOW_RESPONSE=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/flows/instances/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json")

    AUTH_FLOW_UUID=$(echo $FLOW_RESPONSE | jq -r '.results[]? | select(.slug=="default-provider-authorization-implicit-consent") | .pk')

    if [ -z "$AUTH_FLOW_UUID" ] || [ "$AUTH_FLOW_UUID" = "null" ]; then
        echo "❌ Failed to get authorization flow UUID"
        echo "Flow Response:"
        echo "$FLOW_RESPONSE"
        exit 1
    fi

    echo "✅ Found authorization flow UUID: $AUTH_FLOW_UUID"

    # Create OAuth2 Provider
    echo "💡 Creating OAuth2 Provider..."

    PROVIDER_RESPONSE=$(curl -s -X POST "$AUTHENTIK_URL/api/v3/providers/oauth2/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"Mycelium OAuth Provider\",
            \"authorization_flow\": \"$AUTH_FLOW_UUID\",
            \"access_token_validity\": \"minutes=10\",
            \"refresh_token_validity\": \"days=30\",
            \"client_type\": \"confidential\",
            \"include_claims_in_id_token\": true,
            \"sub_mode\": \"hashed_user_id\",
            \"issuer_mode\": \"global\",
            \"application\": \"$APP_UUID\"
        }")

    PROVIDER_ID=$(echo $PROVIDER_RESPONSE | jq -r '.pk')

    if [ -z "$PROVIDER_ID" ] || [ "$PROVIDER_ID" = "null" ]; then
        echo "❌ Failed to create OAuth2 Provider"
        echo "$PROVIDER_RESPONSE"
        exit 1
    fi
    echo "✅ OAuth2 Provider created with ID: $PROVIDER_ID"
else
    echo "✅ Found existing OAuth2 provider with ID: $PROVIDER_ID"
    
    # Update the existing provider to ensure it's linked to our application
    echo "💡 Updating existing provider..."
    PROVIDER_RESPONSE=$(curl -s -X PATCH "$AUTHENTIK_URL/api/v3/providers/oauth2/$PROVIDER_ID/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"application\": \"$APP_UUID\"
        }")
fi

# Get the latest provider details
echo "💡 Getting latest provider details..."
PROVIDER_RESPONSE=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/providers/oauth2/$PROVIDER_ID/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json")

# Extract credentials with error checking
CLIENT_ID=$(echo "$PROVIDER_RESPONSE" | jq -r '.client_id // empty')
if [ -z "$CLIENT_ID" ]; then
    echo "❌ Failed to extract client_id from response"
    exit 1
fi

CLIENT_SECRET=$(echo "$PROVIDER_RESPONSE" | jq -r '.client_secret // empty')
if [ -z "$CLIENT_SECRET" ]; then
    echo "❌ Failed to extract client_secret from response"
    exit 1
fi

# Save credentials to a file for later use
echo "💡 Saving OAuth credentials..."
cat > .oauth_creds.json << EOF
{
    "client_id": "$CLIENT_ID",
    "client_secret": "$CLIENT_SECRET"
}
EOF

echo "✅ Setup complete!"
echo "📋 OAuth Credentials:"
echo "🔑 Client ID: $CLIENT_ID"
echo "🔑 Client Secret: $CLIENT_SECRET"
echo "💡 Credentials have been saved to .oauth_creds.json"
