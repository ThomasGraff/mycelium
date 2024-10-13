import os
from typing import List


class Settings:
    """
    Configuration settings for the application.

    This class holds the configuration settings for the application, including
    database connection details, LLM API information, and server configuration.
    It uses environment variables with default values.
    """

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app/database/mycelium.db")
    DEFAULT_HOST: str = "0.0.0.0"
    DEFAULT_PORT: int = 8000
    DEFAULT_WORKERS: int = 4
    ALLOWED_ORIGINS: List[str] = ["*"]
    LOG_LEVEL: str = "INFO"


settings = Settings()
