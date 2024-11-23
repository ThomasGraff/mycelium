# Step 1: Use Python 3.12 as the base image
FROM python:3.12-slim

# Build-time arguments with default values
ARG BACKEND_HOST=0.0.0.0
ARG BACKEND_PORT=8000
ARG DATABASE_TYPE=supabase
ARG SUPABASE_URL
ARG SUPABASE_KEY

# Set environment variables
ENV DATABASE_TYPE=${DATABASE_TYPE} \
    SUPABASE_URL=${SUPABASE_URL} \
    SUPABASE_KEY=${SUPABASE_KEY}
    
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

# Step 9: Switch to non-root user
USER nobody

# Step 10: Expose the FastAPI app port
EXPOSE 8000

# Step 11: Command to run the FastAPI app
CMD ["sh", "-c", "uvicorn app.main:app --host $BACKEND_HOST --port $BACKEND_PORT"]