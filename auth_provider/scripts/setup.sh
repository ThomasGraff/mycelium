#!/bin/bash

# Set bash to exit on error
set -e

# Variables
AUTHENTIK_URL="http://${AUTHENTIK_HOST}:${AUTHENTIK_PORT}"
MAX_RETRIES=50
RETRY_INTERVAL=15
APP_SLUG="mycelium"

echo "💡 Starting Authentik setup..."

# Check requirements
for cmd in curl jq; do
    if ! command -v $cmd >/dev/null 2>&1; then
        echo "❌ Required command '$cmd' is not installed"
        exit 1
    fi
done

for var in AUTHENTIK_ADMIN_TOKEN AUTHENTIK_HOST AUTHENTIK_PORT; do
    if [ -z "${!var}" ]; then
        echo "❌ Required environment variable '$var' is not set"
        exit 1
    fi
done

# Check Authentik health
retry_count=0
while [ $retry_count -lt $MAX_RETRIES ]; do
    if curl -sSf "$AUTHENTIK_URL/-/health/live/" > /dev/null 2>&1; then
        echo "✅ Authentik is up and running"
        break
    fi
    printf "⚠️  Waiting for Authentik to be ready... (%d/%d)\n" "$((retry_count + 1))" "${MAX_RETRIES}"
    sleep $RETRY_INTERVAL
    retry_count=$((retry_count + 1))
done

if [ $retry_count -eq $MAX_RETRIES ]; then
    echo "❌ Authentik failed to become ready within the timeout period"
    exit 1
fi

# Get authorization flow
flow_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/flows/instances/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json")

auth_flow_uuid=$(echo "$flow_response" | jq -r '.results[] | select(.slug=="default-provider-authorization-implicit-consent") | .pk')

if [ -z "$auth_flow_uuid" ]; then
    echo "❌ Failed to get authorization flow UUID"
    exit 1
fi

echo "✅ Found authorization flow"

# Check for existing provider
existing_provider_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/providers/oauth2/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json")

provider_id=$(echo "$existing_provider_response" | jq -r '.results[] | select(.name=="Mycelium OAuth Provider") | .pk')

# Create provider if it doesn't exist
if [ -z "$provider_id" ] || [ "$provider_id" = "null" ]; then
    echo "💡 Creating new OAuth provider..."
    
    provider_response=$(curl -s -X POST "$AUTHENTIK_URL/api/v3/providers/oauth2/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"Mycelium OAuth Provider\",
            \"authorization_flow\": \"$auth_flow_uuid\",
            \"invalidation_flow\": \"$auth_flow_uuid\",
            \"access_token_validity\": \"minutes=10\",
            \"refresh_token_validity\": \"days=30\",
            \"client_type\": \"confidential\",
            \"include_claims_in_id_token\": true,
            \"sub_mode\": \"hashed_user_id\",
            \"issuer_mode\": \"global\",
            \"redirect_uris\": []
        }")
    
    provider_id=$(echo "$provider_response" | jq -r '.pk')
    if [ -z "$provider_id" ] || [ "$provider_id" = "null" ]; then
        echo "❌ Failed to create OAuth provider"
        exit 1
    fi
    echo "✅ Created OAuth provider"
else
    echo "✅ Found existing OAuth provider"
fi

# Check for existing application
existing_app_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/core/applications/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -G --data-urlencode "slug=$APP_SLUG")

app_uuid=$(echo "$existing_app_response" | jq -r ".results[] | select(.slug==\"$APP_SLUG\") | .pk")

# Create application if it doesn't exist
if [ -z "$app_uuid" ] || [ "$app_uuid" = "null" ]; then
    echo "💡 Creating new application..."
    
    app_response=$(curl -s -X POST "$AUTHENTIK_URL/api/v3/core/applications/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"Mycelium\",
            \"slug\": \"$APP_SLUG\",
            \"provider\": $provider_id,
            \"meta_description\": \"Mycelium Application\",
            \"meta_publisher\": \"Mycelium\",
            \"policy_engine_mode\": \"all\",
            \"open_in_new_tab\": false
        }")
    
    app_uuid=$(echo "$app_response" | jq -r '.pk')
    if [ -z "$app_uuid" ] || [ "$app_uuid" = "null" ]; then
        echo "❌ Failed to create application"
        exit 1
    fi
    echo "✅ Created application"
else
    echo "✅ Found existing application"
fi

# Get the final provider details and credentials
provider_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/providers/oauth2/$provider_id/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json")

# Extract credentials
client_id=$(echo "$provider_response" | jq -r '.client_id')
client_secret=$(echo "$provider_response" | jq -r '.client_secret')

if [ -z "$client_id" ] || [ "$client_id" = "null" ] || [ -z "$client_secret" ] || [ "$client_secret" = "null" ]; then
    echo "❌ Failed to extract OAuth credentials"
    exit 1
fi

# Save credentials
echo "{
  \"client_id\": \"$client_id\",
  \"client_secret\": \"$client_secret\"
}" > .oauth_creds.json

echo "✅ Setup complete!"
echo "📋 OAuth credentials have been saved to .oauth_creds.json" 