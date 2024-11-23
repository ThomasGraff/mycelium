import logging
from typing import Generator, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError

from ..utils.config import settings
from ..@supabase.client import supabase_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)


class DatabaseManager:
    """
    Manages database operations including creation, table setup, and session handling.

    This class implements the Singleton pattern to ensure only one instance
    of DatabaseManager is created throughout the application's lifecycle.
    """

    _instance = None
    Base = declarative_base()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_url: str = settings.DATABASE_URL):
        """
        Initializes the DatabaseManager.

        :param str db_url: The database URL to connect to.
        """
        if not hasattr(self, "initialized"):  # Ensure initialization happens only once
            self.db_url = db_url
            self.engine = None
            self.SessionLocal = None
            self.initialized = True
            self.db_type = settings.DATABASE_TYPE

    def setup_engine(self) -> None:
        """Sets up the database engine based on configuration."""
        if self.db_type == "supabase":
            # Initialize Supabase client
            supabase_client.initialize_client()
        else:
            # Setup SQLAlchemy engine for SQLite
            self.engine = create_engine(self.db_url, echo=False)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self) -> Generator[Session, None, None]:
        """Creates a new database session."""
        if self.db_type == "supabase":
            try:
                yield supabase_client.client
                logger.info(" 💡 Supabase session created")
            except Exception as e:
                logger.error(f" ❌ Supabase operation failed: {str(e)}")
            finally:
                logger.info(" 💡 Supabase session closed")
        else:
            if not self.SessionLocal:
                raise RuntimeError("Database engine not initialized. Call setup_engine() first.")

            db = self.SessionLocal()
            try:
                yield db
                logger.info(" 💡 Database session created")
            except OperationalError as e:
                logger.error(f" ❌ Database operation failed: {str(e)}")
            finally:
                db.close()
                logger.info(" 💡 Database session closed")


db_manager = DatabaseManager()
