import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data_contracts.db")
    LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:8000/llm")
    LLM_API_KEY = os.getenv("LLM_API_KEY", "your_llm_api_key")

settings = Settings()
