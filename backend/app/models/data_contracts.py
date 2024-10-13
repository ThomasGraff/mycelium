from typing import Any, Dict, List, Optional

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database.manager import db_manager


class DataContract(db_manager.Base):
    """
    Represents a Data Contract in the database.

    This model stores information about data contracts, including their specifications,
    metadata, and associated details. It maps to the 'data_contracts' table in the database.
    """

    __tablename__ = "data_contracts"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    data_contract_specification: Mapped[str] = mapped_column(String, nullable=False)
    info_title: Mapped[str] = mapped_column(String, nullable=False)
    info_version: Mapped[str] = mapped_column(String, nullable=False)
    info_description: Mapped[Optional[str]] = mapped_column(String)
    info_owner: Mapped[Optional[str]] = mapped_column(String)
    info_contact: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    servers: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSON)
    terms: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    models: Mapped[Dict[str, Any]] = mapped_column(JSON)
    examples: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSON)
    service_levels: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    links: Mapped[Optional[Dict[str, str]]] = mapped_column(JSON)
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON)

    def __repr__(self) -> str:
        """
        Returns a string representation of the DataContract object.
        :return str: A string representation of the DataContract object.
        """
        return f"<DataContract(id='{self.id}', title='{self.info_title}', version='{self.info_version}')>"
