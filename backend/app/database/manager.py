import logging
from typing import Generator
from ..utils.config import settings
from ..supabase.client import supabase_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)

class DatabaseManager:
    """
    Manages database operations including creation, table setup, and session handling.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initializes the DatabaseManager."""
        if not hasattr(self, "initialized"):
            self.initialized = True

    def get_db(self) -> Generator:
        """Creates a new database session."""
        try:
            yield supabase_client.client
            logger.info(" 💡 Supabase session created")
        except Exception as e:
            logger.error(f" ❌ Supabase operation failed: {str(e)}")
        finally:
            logger.info(" 💡 Supabase session closed")

db_manager = DatabaseManager()
