#!/bin/bash

# Main setup script for Authentik integration

# Set bash to exit on error
set -e

# Source utility functions and other scripts
SCRIPT_DIR="$(dirname "$0")"
source "${SCRIPT_DIR}/authentik_utils.sh"
source "${SCRIPT_DIR}/create_oauth_provider.sh"
source "${SCRIPT_DIR}/create_application.sh"

# Variables
AUTHENTIK_URL="http://${AUTHENTIK_HOST}:${AUTHENTIK_PORT}"
MAX_RETRIES=50
RETRY_INTERVAL=15
APP_SLUG="mycelium"

main() {
    check_requirements
    check_authentik_health || exit 1
    
    echo "✅ Using bootstrap admin token"
    
    # Get authorization flow
    local auth_flow_uuid
    auth_flow_uuid=$(get_authorization_flow)
    [ $? -eq 0 ] || exit 1
    echo "✅ Found authorization flow UUID: $auth_flow_uuid"
    
    # Create or get provider first
    local provider_id
    provider_id=$(get_existing_provider)
    provider_status=$?
    
    if [ $provider_status -ne 0 ] || [ -z "$provider_id" ] || [ "$provider_id" = "null" ]; then
        echo "💡 No existing provider found, creating new one..."
        provider_id=$(create_oauth_provider "$auth_flow_uuid")
        if [ $? -ne 0 ] || [ -z "$provider_id" ]; then
            echo "❌ Failed to create OAuth provider"
            exit 1
        fi
        echo "✅ OAuth2 Provider created with ID: $provider_id"
    else
        echo "✅ Found existing OAuth2 provider with ID: $provider_id"
    fi
    
    # Create or update application with provider
    local app_uuid
    app_uuid=$(get_existing_application)
    
    if [ -z "$app_uuid" ] || [ "$app_uuid" = "null" ]; then
        app_uuid=$(create_application "$provider_id")
        [ $? -eq 0 ] || exit 1
        echo "✅ Application created with UUID: $app_uuid"
    else
        echo "✅ Found existing application with UUID: $app_uuid"
    fi
    
    # Get the final provider details and credentials
    local provider_response
    provider_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/providers/oauth2/$provider_id/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json")

    # Extract and save credentials
    local client_id
    client_id=$(echo "$provider_response" | jq -r '.client_id // empty')
    [ -n "$client_id" ] || { echo "❌ Failed to extract client_id"; exit 1; }

    local client_secret
    client_secret=$(echo "$provider_response" | jq -r '.client_secret // empty')
    [ -n "$client_secret" ] || { echo "❌ Failed to extract client_secret"; exit 1; }

    # Save credentials
    echo "{
      \"client_id\": \"$client_id\",
      \"client_secret\": \"$client_secret\"
    }" > .oauth_creds.json

    echo "✅ Setup complete!"
    echo "📋 OAuth Credentials:"
    echo "🔑 Client ID: $client_id"
    echo "🔑 Client Secret: $client_secret"
    echo "💡 Credentials have been saved to .oauth_creds.json"
}

main "$@" 