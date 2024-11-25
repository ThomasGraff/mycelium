# Step 1: Use Python 3.12 as the base image
FROM python:3.12-slim

# Set environment variables with default values
ARG BACKEND_PORT
ARG AUTHENTIK_HOST
ARG AUTHENTIK_PORT
ARG DATABASE_URL
ARG ACCESS_TOKEN_EXPIRE_MINUTES

ENV AUTHENTIK_HOST=${AUTHENTIK_HOST} \
    AUTHENTIK_PORT=${AUTHENTIK_PORT} \
    BACKEND_PORT=${BACKEND_PORT} \
    DATABASE_URL=${DATABASE_URL} \
    ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}

# Required additional environment variables to add at runtime:
# AUTHENTIK_CLIENT_ID
# AUTHENTIK_CLIENT_SECRET
# SECRET_KEY

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
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

# Step 10: Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${BACKEND_PORT}/health || exit 1

# Step 11: Switch to non-root user
USER nobody

# Step 12: Expose the FastAPI app port
EXPOSE ${BACKEND_PORT}

# Step 13: Command to run the FastAPI app
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT"]