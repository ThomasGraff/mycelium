from sqlalchemy.orm import Session
from .models.data_contract import DataContract
from ..schemas.data_contract import DataContractCreate

def create_data_contract(db: Session, data_contract: DataContractCreate):
    db_data_contract = DataContract(**data_contract.dict())
    db.add(db_data_contract)
    db.commit()
    db.refresh(db_data_contract)
    return db_data_contract

def get_data_contract(db: Session, data_contract_id: int):
    return db.query(DataContract).filter(DataContract.id == data_contract_id).first()

def get_data_contracts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DataContract).offset(skip).limit(limit).all()
