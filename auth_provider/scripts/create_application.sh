#!/bin/bash

# Script to create or update application

create_application() {
    local provider_id=$1
    
    echo "💡 Creating new application..."
    local application_response
    application_response=$(curl -s -X POST "$AUTHENTIK_URL/api/v3/core/applications/" \
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

    local app_uuid
    app_uuid=$(echo $application_response | jq -r '.pk')

    if [ -z "$app_uuid" ] || [ "$app_uuid" = "null" ]; then
        echo "❌ Failed to create Application"
        echo "$application_response"
        return 1
    fi
    
    echo "$app_uuid"
}

get_existing_application() {
    local existing_app_response
    existing_app_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/core/applications/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -G --data-urlencode "slug=$APP_SLUG")

    local app_uuid
    app_uuid=$(echo $existing_app_response | jq -r ".results[] | select(.slug==\"$APP_SLUG\") | .pk")
    
    echo "$app_uuid"
} 