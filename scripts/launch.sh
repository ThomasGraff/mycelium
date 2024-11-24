#!/bin/bash

set -e

# Start Authentik services first
echo "🚀 Starting Authentik services..."
cd auth_provider
./scripts/launch.sh

# Check if setup was successful and get credentials
cd ..
if [ -f "auth_provider/.oauth_creds.json" ]; then
    echo "✅ Setup completed successfully"
    # Export credentials as environment variables
    export AUTHENTIK_CLIENT_ID=$(jq -r '.client_id' auth_provider/.oauth_creds.json)
    export AUTHENTIK_CLIENT_SECRET=$(jq -r '.client_secret' auth_provider/.oauth_creds.json)

    # Modify the two lines in-place without creating backup files
    sed -i "s|^AUTHENTIK_CLIENT_ID=.*|AUTHENTIK_CLIENT_ID=$AUTHENTIK_CLIENT_ID|" .env
    sed -i "s|^AUTHENTIK_CLIENT_SECRET=.*|AUTHENTIK_CLIENT_SECRET=$AUTHENTIK_CLIENT_SECRET|" .env
    
    # Start frontend and backend services
    echo "🚀 Starting frontend and backend services..."
    docker compose --env-file .env up -d
    
    echo "✅ All services have been started successfully!"
else
    echo "❌ Setup failed - credentials file not found"
    exit 1
fi