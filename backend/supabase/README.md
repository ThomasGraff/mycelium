# Supabase Configuration for Mycelium

Ce dossier contient la configuration Supabase pour le projet Mycelium.

## Structure

```
supabase/
├── docker/             # Fichiers Docker
├── config/             # Configuration et scripts d'initialisation
└── docker-compose.yml  # Configuration des services
```

## Installation

1. Copiez le fichier d'environnement exemple :
```bash
cp config/.env.example .env
```

2. Modifiez les variables dans `.env` selon vos besoins

3. Démarrez Supabase :
```bash
docker-compose up -d
```

## Services disponibles

- Studio Supabase : http://localhost:54322
- API REST : http://localhost:54321
- Auth : http://localhost:54324
- Storage : http://localhost:54326

## Base de données

Le script d'initialisation (`config/init.sql`) configure :
- La table data_contracts
- Les politiques de sécurité (RLS)
- Les triggers nécessaires

## Accès au Studio

- URL : http://localhost:54322
- Identifiants par défaut : 
  - Username: admin
  - Password: admin 