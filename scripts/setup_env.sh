#!/bin/bash

set -e  # Exit on error

# Print banner
echo "🔧 Setting up environment variables..."

# Copy .env_example to .env
cp .env_example .env
echo "✨ Created new .env file from template"

# Generate secrets
echo "🔑 Generating secure secrets..."

# Function to generate and validate secrets
generate_secret() {
    local result
    case "$1" in
        "base64")
            result=$(openssl rand -base64 "$2" | tr -d '\n/' | cut -c1-"$2")
            ;;
        "hex")
            result=$(openssl rand -hex "$2")
            ;;
    esac
    echo "$result"
}

# Generate all secrets
AUTHENTIK_SECRET_KEY=$(generate_secret "base64" 60)
AUTHENTIK_ADMIN_PASSWORD=$(generate_secret "base64" 16)
AUTHENTIK_ADMIN_TOKEN=$(generate_secret "hex" 32)
PG_PASS=$(generate_secret "base64" 36)
SECRET_KEY=$(generate_secret "base64" 36)

# Function to update env file safely
update_env_var() {
    local key=$1
    local value=$2
    local escaped_value=$(echo "$value" | sed 's/[\/&]/\\&/g')
    
    # Use different delimiters if value contains forward slashes
    if echo "$value" | grep -q "/"; then
        sed -i "s|^$key=.*|$key=$escaped_value|" .env
    else
        sed -i "s/$key=.*/$key=$escaped_value/" .env
    fi
    
    # Verify the replacement
    if ! grep -q "^$key=$escaped_value" .env; then
        echo "❌ Failed to update $key in .env file"
        return 1
    fi
    echo "✅ Successfully set $key"
}

# Update all variables
echo "📝 Updating environment variables..."
update_env_var "AUTHENTIK_SECRET_KEY" "$AUTHENTIK_SECRET_KEY"
update_env_var "AUTHENTIK_ADMIN_PASSWORD" "$AUTHENTIK_ADMIN_PASSWORD"
update_env_var "AUTHENTIK_ADMIN_TOKEN" "$AUTHENTIK_ADMIN_TOKEN"
update_env_var "PG_PASS" "$PG_PASS"
update_env_var "SECRET_KEY" "$SECRET_KEY"

# Verify .env file was created and has content
if [ ! -s .env ]; then
    echo "❌ Error: .env file is empty or was not created properly"
    exit 1
fi

echo "✅ Environment setup complete!"
echo "📝 Your .env file has been created with secure random values"
echo "⚠️ Please review the .env file and modify any other values as needed"

