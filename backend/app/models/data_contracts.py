from sqlalchemy import JSON, Column, String

from ..database import Base


class DataContract(Base):
    """
    Represents a Data Contract in the database.

    This model stores information about data contracts, including their specifications,
    metadata, and associated details. It maps to the 'data_contracts' table in the database.
    """

    __tablename__ = "data_contracts"

    id = Column(String, primary_key=True, index=True)
    data_contract_specification = Column(String, nullable=False)
    info_title = Column(String, nullable=False)
    info_version = Column(String, nullable=False)
    info_description = Column(String)
    info_owner = Column(String)
    info_contact = Column(JSON)
    servers = Column(JSON)
    terms = Column(JSON)
    models = Column(JSON)
    examples = Column(JSON)
    servicelevels = Column(JSON)
    links = Column(JSON)
    tags = Column(JSON)

    def __repr__(self) -> str:
        """
        Returns a string representation of the DataContract object.
        :return str: A string representation of the DataContract object.
        """
        return f"<DataContract(id='{self.id}', title='{self.info_title}', version='{self.info_version}')>"
