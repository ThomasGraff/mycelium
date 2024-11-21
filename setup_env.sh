#!/bin/bash

# Print banner
echo "🔧 Setting up environment variables..."

# Copy .env_example to .env
cp .env_example .env

# Generate secrets
echo "🔑 Generating secure secrets..."

# Generate secrets with proper line handling
AUTHENTIK_SECRET_KEY=$(openssl rand -base64 60 | tr -d '\n/' | cut -c1-60)
echo "✨ Generated Authentik secret key"

# Generate AUTHENTIK_ADMIN_PASSWORD
AUTHENTIK_ADMIN_PASSWORD=$(openssl rand -base64 16 | tr -d '\n/')
echo "✨ Generated Authentik admin password"

# Generate AUTHENTIK_ADMIN_TOKEN
AUTHENTIK_ADMIN_TOKEN=$(openssl rand -hex 32 | tr -d '\n/')
echo "✨ Generated Authentik admin token"

# Generate PG_PASS
PG_PASS=$(openssl rand -base64 36 | tr -d '\n/')
echo "✨ Generated PostgreSQL password"

# Generate SECRET_KEY for JWT
SECRET_KEY=$(openssl rand -base64 36 | tr -d '\n/')
echo "✨ Generated JWT secret key"

# Function to escape special characters for sed
escape_sed() {
    echo "$1" | sed -e 's/[\/&]/\\&/g'
}

# Escape the generated values
AUTHENTIK_SECRET_KEY_ESCAPED=$(escape_sed "$AUTHENTIK_SECRET_KEY")
AUTHENTIK_ADMIN_PASSWORD_ESCAPED=$(escape_sed "$AUTHENTIK_ADMIN_PASSWORD")
AUTHENTIK_ADMIN_TOKEN_ESCAPED=$(escape_sed "$AUTHENTIK_ADMIN_TOKEN")
PG_PASS_ESCAPED=$(escape_sed "$PG_PASS")
SECRET_KEY_ESCAPED=$(escape_sed "$SECRET_KEY")

# Replace the empty values in .env with generated secrets using | as delimiter
sed -i "s|^AUTHENTIK_SECRET_KEY=$|AUTHENTIK_SECRET_KEY=$AUTHENTIK_SECRET_KEY_ESCAPED|" .env
sed -i "s|^AUTHENTIK_ADMIN_PASSWORD=$|AUTHENTIK_ADMIN_PASSWORD=$AUTHENTIK_ADMIN_PASSWORD_ESCAPED|" .env
sed -i "s|^AUTHENTIK_ADMIN_TOKEN=$|AUTHENTIK_ADMIN_TOKEN=$AUTHENTIK_ADMIN_TOKEN_ESCAPED|" .env
sed -i "s|^PG_PASS=$|PG_PASS=$PG_PASS_ESCAPED|" .env
sed -i "s|^SECRET_KEY=$|SECRET_KEY=$SECRET_KEY_ESCAPED|" .env

echo "✅ Environment setup complete!"
echo "📝 Your .env file has been created with secure random values"
echo "⚠️  Please review the .env file and modify any other values as needed"
