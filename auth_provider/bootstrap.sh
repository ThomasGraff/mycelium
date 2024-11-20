#!/bin/sh

set -e

# Variables
AUTHENTIK_URL="http://${AUTHENTIK_HOST:-0.0.0.0}:${AUTHENTIK_PORT:-9000}"

# Wait for Authentik to initialize
echo "💡 Waiting for Authentik to initialize..."
until curl -sSf "$AUTHENTIK_URL/if/flow/onboarding/" >/dev/null 2>&1; do
    echo "⚠️  Authentik not ready yet. Retrying in 5 seconds..."
    sleep 5
done
echo "✅ Authentik is ready!"

# Automate onboarding to create the admin user
echo "💡 Running onboarding flow to create the admin user..."
ADMIN_USERNAME="admin"
ADMIN_PASSWORD=$(openssl rand -base64 16)

curl -sSf -X POST "$AUTHENTIK_URL/if/flow/onboarding/" \
    -H "Content-Type: application/json" \
    -d '{
        "password": "'"$ADMIN_PASSWORD"'",
        "username": "'"$ADMIN_USERNAME"'"
    }'

echo "✅ Admin user created. Username: $ADMIN_USERNAME Password: $ADMIN_PASSWORD"

# Write admin credentials to a temporary file for setup.sh
echo "💡 Writing admin credentials to temporary file..."
cat <<EOF > .admin_creds.tmp
ADMIN_USERNAME=$ADMIN_USERNAME
ADMIN_PASSWORD=$ADMIN_PASSWORD
EOF

echo "✅ Bootstrap complete! Run setup.sh to configure the OAuth application."
