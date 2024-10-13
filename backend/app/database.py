import logging
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@event.listens_for(engine, "connect")
def create_tables(dbapi_connection, connection_record):
    """
    Creates tables if they don't exist when a new connection is established.

    :param dbapi_connection: The DBAPI connection.
    :param connection_record: The connection record.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info(" ✅ Database tables created successfully")
    except OperationalError as e:
        logger.error(f" ❌ Failed to create database tables: {str(e)}")


def get_db() -> Generator:
    """
    Creates a new database session and yields it.

    :yield: A SQLAlchemy Session object.
    """
    db = SessionLocal()
    try:
        logger.info(" 💡 Database session created")
        yield db
    except OperationalError as e:
        logger.error(f" ❌ Database operation failed: {str(e)}")
    finally:
        db.close()
        logger.info(" 💡 Database session closed")
