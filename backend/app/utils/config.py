from os import getenv
from typing import Final, List


class Settings:
    """
    Configuration settings for the application.

    This class holds the configuration settings for the application, including
    database connection details, LLM API information, and server configuration.
    It uses environment variables with default values.

    :raises ValueError: If required environment variables are not set
    """

    def __init__(self):
        """Initialize settings and validate required environment variables."""
        # Required environment variables
        self.SECRET_KEY: Final[str] = self._get_required_env("SECRET_KEY")
        self.AUTHENTIK_URL: Final[str] = self._get_required_env("AUTHENTIK_URL")
        self.AUTHENTIK_CLIENT_ID: Final[str] = self._get_required_env("AUTHENTIK_CLIENT_ID")
        self.AUTHENTIK_CLIENT_SECRET: Final[str] = self._get_required_env("AUTHENTIK_CLIENT_SECRET")

        # Optional environment variables with defaults
        self.DATABASE_URL: str = getenv("DATABASE_URL", "sqlite:///./app/database/mycelium.db")
        self.ALLOWED_ORIGINS: List[str] = ["*"]
        self.LOG_LEVEL: str = "INFO"
        self.ALGORITHM: Final[str] = getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    def _get_required_env(self, key: str) -> str:
        """
        Get a required environment variable.

        :param str key: The environment variable key
        :return str: The environment variable value
        :raises ValueError: If the environment variable is not set
        """
        value = getenv(key)
        if value is None:
            raise ValueError(f" ❌ Required environment variable {key} is not set")
        return value


settings = Settings()
