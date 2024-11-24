#!/bin/bash

docker-compose --env-file ../.env up -d

# Run the setup script
echo ""
echo "🔧 Running Authentik setup script..."
chmod +x ./scripts/setup.sh
./scripts/setup.sh