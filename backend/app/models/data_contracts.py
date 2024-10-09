from sqlalchemy import Column, Integer, String
from ..database import Base

class DataContract(Base):
    __tablename__ = "data_contracts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    schema = Column(String)  # Doit respecter les spécifications de datacontract.com
