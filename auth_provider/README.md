# 🔐 Authentik Authentication Provider

## 🐳 Docker Deployment

1. Start Authentik services:
   ```bash
   docker compose --env-file ../.env up -d
   ```

2. Setup OAuth application:
   ```bash
   ./setup.sh
   ```

## 📋 Required Environment Variables

Make sure you have properly set the environment variables in your `.env` file before anything here (see .env_example at the root of the project).

## 🌐 Access

- Admin Interface: `http://localhost:9000`
- HTTPS Interface: `https://localhost:9443`
