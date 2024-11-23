from os import getenv
from typing import Final, List


class Settings:
    """
    Configuration settings for the application.
    """

    def __init__(self):
        """Initialize settings and validate required environment variables."""
        # Required environment variables
        self.SECRET_KEY: Final[str] = self._get_required_env("SECRET_KEY")
        self.SUPABASE_URL: str = self._get_required_env("SUPABASE_URL")
        self.SUPABASE_KEY: str = self._get_required_env("SUPABASE_KEY")

        # Optional environment variables with defaults
        self.DATABASE_TYPE: str = getenv("DATABASE_TYPE", "supabase")
        self.ALLOWED_ORIGINS: List[str] = ["*"]
        self.LOG_LEVEL: str = "INFO"
        self.ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    def _get_required_env(self, key: str) -> str:
        """Get a required environment variable."""
        value = getenv(key)
        if value is None:
            raise ValueError(f" ❌ Required environment variable {key} is not set")
        return value


settings = Settings()
