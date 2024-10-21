# 🚀 Mycelium API



## 🐳 Docker Deployment


1. Build the Docker image:
   ```
   docker build -t mycelium-backend .
   ```

2. Run the Docker container:
   ```
   docker run -p 8000:8000 mycelium-backend
   ```

## Local Development

### 📋 Prerequisites

- 🐍 Python 3.12 or higher
- 📦 Poetry (Python dependency management tool)

### 🛠️ Setup & Run

1. Clone the repository and install dependencies:
   ```
   git clone https://github.com/ThomasGraff/mycelium.git
   cd mycelium/backend
   poetry install
   ```

2. Launch the server:
   ```
   poetry run uvicorn app.main:app --port 8000
   ```


🎉 The backend server will be accessible at `http://localhost:8000`.
