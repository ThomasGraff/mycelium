# 🚀 Mycelium Frontend

## 🐳 Docker Deployment

1. Build the Docker image:
   ```
   docker build -t mycelium-frontend .
   ```

2. Run the Docker container:
   ```
   docker run -p 8080:80 -e BACKEND_URL=http://0.0.0.0:8000 mycelium-frontend
   ```

## Local Development

### 📋 Prerequisites

- 📦 Node.js 18 or higher
- 🧶 Yarn package manager

### 🛠️ Setup & Run

1. Clone the repository and install dependencies:
   ```
   git clone https://github.com/ThomasGraff/mycelium.git
   cd mycelium/frontend/mycelium
   yarn install
   ```

2. Launch the development server:
   ```
   yarn serve
   ```

🎉 The frontend development server will be accessible at `http://localhost:8080`.