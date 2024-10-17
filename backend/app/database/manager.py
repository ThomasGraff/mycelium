import logging
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from ..utils.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger("sqlalchemy.engine").setLevel(settings.LOG_LEVEL)


class DatabaseManager:
    """
    Manages database operations including creation, table setup, and session handling.

    This class implements the Singleton pattern to ensure only one instance
    of DatabaseManager is created throughout the application's lifecycle.
    """

    _instance = None
    Base: DeclarativeMeta = declarative_base()

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

    def create_database(self) -> None:
        """
        Creates the database in the current folder if it doesn't exist.
        """
        db_path = self.db_url.replace("sqlite:///", "")
        if not os.path.exists(db_path):
            try:
                open(db_path, "a").close()
                logger.info(f" ✅ Database file created at {db_path}")
            except IOError as e:
                logger.error(f" ❌ Failed to create database file: {str(e)}")

    def setup_engine(self) -> None:
        """
        Sets up the database engine and session factory.
        """
        self.engine = create_engine(self.db_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self) -> None:
        """
        Creates all tables defined in the SQLAlchemy models.

        This method creates all tables defined in the SQLAlchemy models and logs the names of the created tables.
        """
        if not self.engine:
            raise RuntimeError("Database engine not initialized. Call setup_engine() first.")

        try:
            self.Base.metadata.create_all(bind=self.engine)
            created_tables = self.Base.metadata.tables.keys()
            logger.info(f" ✅ All database tables created successfully: [{', '.join(created_tables)}]")
        except Exception as e:
            logger.error(f" ❌ Failed to create database tables: {str(e)}")

    def get_db(self) -> Generator[Session, None, None]:
        """
        Creates a new database session and yields it.

        :yield: A SQLAlchemy Session object.
        """
        if not self.SessionLocal:
            raise RuntimeError("Database engine not initialized. Call setup_engine() first.")

        db = self.SessionLocal()
        try:
            logger.info(" 💡 Database session created")
            yield db
        except OperationalError as e:
            logger.error(f" ❌ Database operation failed: {str(e)}")
        finally:
            db.close()
            logger.info(" 💡 Database session closed")


db_manager = DatabaseManager()
