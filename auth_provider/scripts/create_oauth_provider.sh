#!/bin/bash

# Script to create or update OAuth provider

create_oauth_provider() {
    local auth_flow_uuid=$1
    local app_uuid=$2

    # Validate input
    if [ -z "$auth_flow_uuid" ]; then
        return 1
    fi
    
    local provider_response
    provider_response=$(curl -s -X POST "$AUTHENTIK_URL/api/v3/providers/oauth2/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"Mycelium OAuth Provider\",
            \"authorization_flow\": \"$auth_flow_uuid\",
            \"access_token_validity\": \"minutes=10\",
            \"refresh_token_validity\": \"days=30\",
            \"client_type\": \"confidential\",
            \"include_claims_in_id_token\": true,
            \"sub_mode\": \"hashed_user_id\",
            \"issuer_mode\": \"global\"
        }")

    # Check if the response is valid JSON
    if ! echo "$provider_response" | jq empty 2>/dev/null; then
        return 1
    fi

    local provider_id
    provider_id=$(echo "$provider_response" | jq -r '.pk // empty')

    if [ -z "$provider_id" ] || [ "$provider_id" = "null" ]; then
        return 1
    fi
    
    echo "$provider_id"
}

get_existing_provider() {
    local existing_provider_response
    existing_provider_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/providers/oauth2/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json")

    # Check if the response is valid JSON
    if ! echo "$existing_provider_response" | jq empty 2>/dev/null; then
        return 1
    fi

    # First try to find provider by name
    local provider_id
    provider_id=$(echo "$existing_provider_response" | jq -r '.results[] | select(.name=="Mycelium OAuth Provider") | .pk')

    echo "$provider_id"
}

# Export the functions so they can be used by other scripts
export -f create_oauth_provider
export -f get_existing_provider