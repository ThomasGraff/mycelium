#!/bin/bash

# Common utilities and checks for Authentik scripts

check_authentik_health() {
    local authentik_url="${AUTHENTIK_URL}/-/health/live/"
    local retry_count=0
    
    while [ $retry_count -lt $MAX_RETRIES ]; do
        if curl -sSf "${authentik_url}" > /dev/null 2>&1; then
            echo "✅ Authentik is up and running"
            return 0
        fi
        printf "⚠️ Waiting for Authentik to be ready... (%d/%d)\n" "${retry_count}" "${MAX_RETRIES}"
        sleep $RETRY_INTERVAL
        retry_count=$((retry_count + 1))
    done
    
    echo "❌ Authentik failed to become ready within the timeout period"
    return 1
}

check_requirements() {
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
}

get_authorization_flow() {
    local flow_response
    local auth_flow_uuid
    
    flow_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/flows/instances/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json")

    auth_flow_uuid=$(echo $flow_response | jq -r '.results[]? | select(.slug=="default-provider-authorization-implicit-consent") | .pk')

    if [ -z "$auth_flow_uuid" ] || [ "$auth_flow_uuid" = "null" ]; then
        echo "❌ Failed to get authorization flow UUID"
        echo "Flow Response:"
        echo "$flow_response"
        return 1
    fi

    echo "$auth_flow_uuid"
} 