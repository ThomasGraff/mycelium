# 🚀 Backend for Mycelium


## 📋 Prerequisites

- 🐍 Python 3.12 or higher
- 📦 Poetry (Python dependency management tool)

## 🛠️ Setup

1. Clone the repository and install dependencies:
   ```
   git clone https://github.com/ThomasGraff/mycelium.git
   cd mycelium/backend
   poetry install
   ```

## 🏃‍♂️ Run

1. Navigate to the backend directory and launch the server:
    ```
    cd backend
    poetry run uvicorn app.main:app --port 8000
    ```


## 📚 Documentation

The documentation uses MkDocs to generate dynamically the documentation from the pydantic models. It includes detailed information about the Data Contract models and their usage. To view it:  

1. Navigate to the `docs` directory and launch the documentation server:
   ```
   cd backend/docs
   mkdocs serve --dev-addr=127.0.0.1:8000
   ```


