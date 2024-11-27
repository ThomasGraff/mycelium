#!/bin/bash

echo "🚀 Starting Authentik services..."
docker compose --env-file ../.env up -d

# Run the setup script
echo ""
chmod +x ./scripts/setup.sh
./scripts/setup.sh


# Check if setup was successful and get credentials
if [ -f ".oauth_creds.json" ]; then

    # Export credentials as environment variables
    export AUTHENTIK_CLIENT_ID=$(jq -r '.client_id' .oauth_creds.json)
    export AUTHENTIK_CLIENT_SECRET=$(jq -r '.client_secret' .oauth_creds.json)

    # Modify the two lines in-place without creating backup files
    # Use different sed syntax for Mac vs Linux
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|^AUTHENTIK_CLIENT_ID=.*|AUTHENTIK_CLIENT_ID=$AUTHENTIK_CLIENT_ID|" ../.env
        sed -i '' "s|^AUTHENTIK_CLIENT_SECRET=.*|AUTHENTIK_CLIENT_SECRET=$AUTHENTIK_CLIENT_SECRET|" ../.env
    else
        # Linux
        sed -i "s|^AUTHENTIK_CLIENT_ID=.*|AUTHENTIK_CLIENT_ID=$AUTHENTIK_CLIENT_ID|" ../.env
        sed -i "s|^AUTHENTIK_CLIENT_SECRET=.*|AUTHENTIK_CLIENT_SECRET=$AUTHENTIK_CLIENT_SECRET|" ../.env
    fi
    echo "✅ Authentik setup completed successfully"
else
    exit 1
fi