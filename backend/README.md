# 🚀 Mycelium API

## 💾 Database Configuration

L'application supporte deux options de base de données :

### SQLite (Par défaut)
Dans votre fichier .env :
```
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:///./app/database/mycelium.db
```

### Supabase
Pour utiliser Supabase localement :

1. Créez un fichier `.env` dans le dossier backend :
```
DATABASE_TYPE=supabase
POSTGRES_PASSWORD=your-super-secret-password
JWT_SECRET=your-super-secret-jwt-token
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=admin
SUPABASE_URL=http://localhost:54321
SUPABASE_KEY=your-supabase-anon-key
```

2. Démarrez l'environnement de développement avec Supabase :
```bash
docker-compose up -d
```

3. Accédez au Studio Supabase :
   - URL : http://localhost:54322
   - Identifiants : admin/admin (ou vos credentials configurés)

## 🐳 Docker Deployment

### Développement local avec Docker

1. Démarrer l'environnement complet :
```bash
docker-compose up -d
```

2. Les services seront disponibles aux adresses suivantes :
   - Backend API : http://localhost:8000
   - Supabase API : http://localhost:54321
   - Supabase Studio : http://localhost:54322

### Production

1. Build de l'image Docker :
```bash
docker build -t mycelium-backend .
```

2. Lancement du conteneur :
```bash
docker run -p 8000:8000 mycelium-backend
```

## 💻 Développement Local Sans Docker

### 📋 Prérequis

- 🐍 Python 3.12 ou supérieur
- 📦 Poetry (gestionnaire de dépendances Python)

### 🛠️ Installation & Lancement

1. Clonez le dépôt et installez les dépendances :
```bash
git clone https://github.com/ThomasGraff/mycelium.git
cd mycelium/backend
poetry install
```

2. Lancez le serveur :
```bash
poetry run uvicorn app.main:app --port 8000
```

🎉 Le serveur backend sera accessible à l'adresse `http://localhost:8000`.

## 📝 Notes

- Pour le développement local, le docker-compose inclut une instance Supabase complète
- Les données Supabase sont persistées dans un volume Docker
- Le Studio Supabase permet de gérer facilement la base de données et les API
