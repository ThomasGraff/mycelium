import os
from os import getenv
from typing import Final, List


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

    # Auth Configuration
    SECRET_KEY: Final[str] = getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: Final[str] = getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Authentik Configuration
    AUTHENTIK_URL: Final[str] = getenv("AUTHENTIK_URL", "https://auth.example.com")
    AUTHENTIK_CLIENT_ID: Final[str] = getenv("AUTHENTIK_CLIENT_ID", "")
    AUTHENTIK_CLIENT_SECRET: Final[str] = getenv("AUTHENTIK_CLIENT_SECRET", "")


settings = Settings()
