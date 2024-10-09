from fastapi import FastAPI
from .api import data_contracts
from .database import engine, Base
from .config import settings  # Importez vos configurations

# Créer les tables de la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(data_contracts.router, prefix="/data_contracts", tags=["data_contracts"])
