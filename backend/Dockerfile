# Step 1: Use Python 3.12 as the base image
FROM python:3.12-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Install Poetry and configure it
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Step 5: Copy Poetry files
COPY pyproject.toml poetry.lock* ./

# Step 6: Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Step 7: Copy the application code
COPY . .

# Step 8: Install the project
RUN poetry install --no-interaction --no-ansi

# Modifications pour la sécurité et la configuration
# Step 9: Create necessary directories
RUN mkdir -p /app/app/database && \
    chown -R nobody:nogroup /app/app/database && \
    chmod 770 /app/app/database

# Step 10: Set environment variables
ENV BACKEND_HOST=0.0.0.0
ENV BACKEND_PORT=8000
ENV AUTHENTIK_HOST=authentik.local
ENV AUTHENTIK_PORT=80
# Ajout de variables importantes pour l'authentification
ENV AUTHENTIK_CLIENT_ID=""
ENV AUTHENTIK_CLIENT_SECRET=""

# Step 11: Switch to non-root user
USER nobody

# Step 12: Expose the FastAPI app port
EXPOSE 8000

# Step 13: Command to run the FastAPI app
CMD ["sh", "-c", "uvicorn app.main:app --host $BACKEND_HOST --port $BACKEND_PORT"]