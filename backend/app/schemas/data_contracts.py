from pydantic import BaseModel

class DataContractBase(BaseModel):
    name: str
    description: str
    schema: str  # Doit respecter les spécifications de datacontract.com

class DataContractCreate(DataContractBase):
    pass

class DataContract(DataContractBase):
    id: int

    class Config:
        orm_mode = True
