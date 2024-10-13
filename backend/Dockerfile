# Step 1: Use Python 3.12 as the base image
FROM python:3.12-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Step 4: Install Poetry
RUN pip install poetry

# Step 5: Copy Poetry files and install dependencies
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-dev

# Step 6: Copy the application code
COPY . .

# Step 7: Expose the FastAPI app port
EXPOSE 8000

# Step 8: Command to run the FastAPI app
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
