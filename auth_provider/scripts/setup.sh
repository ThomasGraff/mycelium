#!/bin/bash

# Set bash to exit on error
set -e

# Variables
AUTHENTIK_URL="http://${AUTHENTIK_HOST}:${AUTHENTIK_PORT}"
MAX_RETRIES=50
RETRY_INTERVAL=15
APP_SLUG="mycelium"
GROUP_NAME="System Users Group"
ROLE_NAME="System User Role"


echo "💡 Launching Authentik setup"

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


# Get authorization flow with retries
echo "💡 Attempting to get authorization flow..."
retry_count=0
auth_flow_uuid=""

while [ $retry_count -lt $MAX_RETRIES ]; do
    flow_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/flows/instances/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json")
    
    auth_flow_uuid=$(echo "$flow_response" | jq -r '.results[] | select(.slug=="default-provider-authorization-implicit-consent") | .pk')
    
    if [ -n "$auth_flow_uuid" ] && [ "$auth_flow_uuid" != "null" ]; then
        echo "✅ Found authorization flow with UUID: $auth_flow_uuid"
        break
    fi
    
    printf "⚠️  Authorization flow not found yet... Retrying (%d/%d)\n" "$((retry_count + 1))" "${MAX_RETRIES}"
    sleep $RETRY_INTERVAL
    retry_count=$((retry_count + 1))
done

if [ -z "$auth_flow_uuid" ] || [ "$auth_flow_uuid" = "null" ]; then
    echo "❌ Failed to get authorization flow UUID after $MAX_RETRIES attempts"
    exit 1
fi


echo "✅ Found authorization flow"

# Check for existing provider
existing_provider_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/providers/oauth2/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json")

provider_id=$(echo "$existing_provider_response" | jq -r '.results[] | select(.name=="Mycelium OAuth Provider") | .pk')

# First, get the standard scope mappings
echo "💡 Fetching standard scope mappings..."
scope_mappings_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/propertymappings/provider/scope/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json")

# Extract the UUIDs of the standard scope mappings
scope_mapping_ids=$(echo "$scope_mappings_response" | jq -r '.results[] | select(.scope_name | IN("openid", "email", "profile", "offline_access", "goauthentik.io/api")) | .pk')

if [ -z "$scope_mapping_ids" ]; then
    echo "❌ Failed to find scope mappings"
    exit 1
fi

# Convert the scope mapping IDs to a JSON array
scope_mappings_json=$(echo "$scope_mapping_ids" | jq -R . | jq -s .)

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
            \"redirect_uris\": [],
            \"property_mappings\": $scope_mappings_json,
            \"token_validity\": \"minutes=10\",
            \"grant_types\": [
                \"client_credentials\",
                \"authorization_code\",
                \"refresh_token\"
            ]
        }")
    provider_id=$(echo "$provider_response" | jq -r '.pk')
    if [ -z "$provider_id" ] || [ "$provider_id" = "null" ]; then
        echo "❌ Failed to create OAuth provider"
        exit 1
    fi
    echo "✅ Created OAuth provider"
else
    echo "💡 Updating existing OAuth provider with scope mappings..."
    provider_update_response=$(curl -s -X PATCH "$AUTHENTIK_URL/api/v3/providers/oauth2/$provider_id/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"property_mappings\": $scope_mappings_json
        }")
    if echo "$provider_update_response" | jq -e '.pk' > /dev/null 2>&1; then
        echo "✅ Updated OAuth provider scope mappings"
    else
        echo "❌ Failed to update OAuth provider scope mappings"
        exit 1
    fi
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


# Create or find the role
echo "💡 Creating or finding role '$ROLE_NAME'..."
role_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/rbac/roles/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -G --data-urlencode "name=$ROLE_NAME")
role_id=$(echo "$role_response" | jq -r --arg ROLE_NAME "$ROLE_NAME" '.results[] | select(.name == $ROLE_NAME) | .pk // empty')

if [ -z "$role_id" ]; then
    echo "💡 Creating role '$ROLE_NAME'..."
    role_response=$(curl -s -X POST "$AUTHENTIK_URL/api/v3/rbac/roles/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"$ROLE_NAME\"
        }")
    role_id=$(echo "$role_response" | jq -r '.pk')
    echo "✅ Created role with ID $role_id"
else
    echo "✅ Found existing role with ID $role_id"
fi

# Assign permissions to the role
echo "💡 Assigning permissions to role '$ROLE_NAME'..."
assign_response=$(curl -s -X POST "$AUTHENTIK_URL/api/v3/rbac/permissions/assigned_by_roles/$role_id/assign/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"permissions\": [
            \"authentik_core.add_user\",
            \"authentik_core.delete_user\",
            \"authentik_core.view_user\",
            \"authentik_core.change_user\",
            \"authentik_core.reset_user_password\",
            \"authentik_stages_user_login.view_userloginstage\",
            \"authentik_stages_user_login.add_userloginstage\",
            \"authentik_stages_user_logout.view_userlogoutstage\",
            \"authentik_stages_user_logout.add_userlogoutstage\",
            \"authentik_core.add_authenticatedsession\",
            \"authentik_core.view_authenticatedsession\",
            \"authentik_core.delete_authenticatedsession\",
            \"authentik_core.add_token\",
            \"authentik_core.view_token\",
            \"authentik_providers_oauth2.add_accesstoken\",
            \"authentik_providers_oauth2.view_accesstoken\",
            \"authentik_providers_oauth2.delete_accesstoken\"
        ]
    }")

# Check if the assignment was successful
if echo "$assign_response" | jq -e 'if type == "array" and length > 0 then true else false end' > /dev/null 2>&1; then
    echo "✅ Permissions assigned to role"
else
    echo "❌ Failed to assign permissions to role"
    echo "Response: $assign_response"
    exit 1
fi


# Create or find the group
echo "💡 Creating or finding group '$GROUP_NAME'..."
group_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/core/groups/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -G --data-urlencode "name=$GROUP_NAME")

group_id=$(echo "$group_response" | jq -r --arg GROUP_NAME "$GROUP_NAME" '.results[] | select(.name == $GROUP_NAME) | .pk // empty')

if [ -z "$group_id" ]; then
    group_response=$(curl -s -X POST "$AUTHENTIK_URL/api/v3/core/groups/" \
        -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"$GROUP_NAME\",
            \"roles\": [\"$role_id\"]
        }")
    group_id=$(echo "$group_response" | jq -r '.pk')
    echo "✅ Created group with ID $group_id"
else
    echo "✅ Found existing group with ID $group_id"
fi

# Trigger system user creation by making a token request
echo "💡 Triggering system user creation..."
token_response=$(curl -s -X POST "$AUTHENTIK_URL/application/o/token/" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=client_credentials&client_id=$client_id&client_secret=$client_secret")

if echo "$token_response" | jq -e '.access_token' > /dev/null 2>&1; then
    echo "✅ Successfully triggered system user creation"
else
    echo "⚠️ Token request completed but may have failed: $token_response"
fi

# Add system users to the group
echo "💡 Adding system users to group '$GROUP_NAME'..."
system_users_response=$(curl -s -X GET "$AUTHENTIK_URL/api/v3/core/users/" \
    -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -G --data-urlencode "username__startswith=ak-")
system_user_ids=$(echo "$system_users_response" | jq -r '.results[] | select(.username!="akadmin") | .pk // empty')

if [ -z "$system_user_ids" ]; then
    echo "❌ No valid system users found to add to group"
else
    count=0
    for user_id in $system_user_ids; do
        curl -s -X PATCH "$AUTHENTIK_URL/api/v3/core/users/$user_id/" \
            -H "Authorization: Bearer $AUTHENTIK_ADMIN_TOKEN" \
            -H "Content-Type: application/json" \
            -d "{\"groups\": [\"$group_id\"]}" > /dev/null
        count=$((count + 1))
    done
    echo "✅ Added $count system user(s) to group '$GROUP_NAME'"
fi

# Save credentials
echo "{
  \"client_id\": \"$client_id\",
  \"client_secret\": \"$client_secret\"
}" > .oauth_creds.json

echo "✅ Setup complete!"
echo "📋 OAuth credentials have been saved to .oauth_creds.json" 