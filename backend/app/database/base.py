from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

T = TypeVar('T')

class DatabaseProvider(ABC):
    """Interface abstraite pour les providers de base de données"""
    
    @abstractmethod
    def get_engine(self) -> Engine:
        """Retourne l'engine SQLAlchemy"""
        pass
    
    @abstractmethod
    def get_session(self) -> Session:
        """Retourne une session de base de données"""
        pass
    
    @abstractmethod
    def init_db(self) -> None:
        """Initialise la base de données"""
        pass

class SQLiteProvider(DatabaseProvider):
    def __init__(self, database_url: str):
        self.database_url = database_url
        self._engine = None
        self._session_factory = None
        
    def get_engine(self) -> Engine:
        if not self._engine:
            self._engine = create_engine(
                self.database_url,
                connect_args={"check_same_thread": False}
            )
        return self._engine
        
    def get_session(self) -> Session:
        if not self._session_factory:
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.get_engine()
            )
        return self._session_factory()
        
    def init_db(self) -> None:
        from app.models.base import Base
        Base.metadata.create_all(bind=self.get_engine())

class PostgreSQLProvider(DatabaseProvider):
    def __init__(self, database_url: str):
        self.database_url = database_url
        self._engine = None
        self._session_factory = None
        
    def get_engine(self) -> Engine:
        if not self._engine:
            self._engine = create_engine(self.database_url)
        return self._engine
        
    def get_session(self) -> Session:
        if not self._session_factory:
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.get_engine()
            )
        return self._session_factory()
        
    def init_db(self) -> None:
        from app.models.base import Base
        Base.metadata.create_all(bind=self.get_engine()) 