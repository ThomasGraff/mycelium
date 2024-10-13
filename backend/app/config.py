import os


class Settings:
    """
    Configuration settings for the application.

    This class holds the configuration settings for the application, including
    database connection details, LLM API information, and server configuration.
    It uses environment variables with default values.
    """

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./mycelium.db")
    LLM_API_URL: str = os.getenv("LLM_API_URL", "http://localhost:8000/llm")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "your_llm_api_key")
    DEFAULT_HOST: str = "0.0.0.0"
    DEFAULT_PORT: int = 8000
    DEFAULT_WORKERS: int = 4


settings = Settings()
