import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..config import settings
from ..models.data_contracts import DataContract as DataContractModel
from ..schemas.data_contract_create import DataContractCreate
from ..schemas.data_contracts import DataContract

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def create_data_contract(db: Session, data_contract: DataContractCreate) -> DataContract:
    """
    Creates a new data contract in the database.

    :param Session db: The database session.
    :param DataContractCreate data_contract: The data contract to be created.
    :return DataContract: The created data contract.
    :raises SQLAlchemyError: If there's an error during database operations.
    :raises Exception: If there's any other unexpected error.
    """
    try:
        db_data_contract = DataContractModel(
            id=data_contract.id,
            data_contract_specification=data_contract.data_contract_specification,
            info_title=data_contract.info.title,
            info_version=data_contract.info.version,
            info_description=data_contract.info.description,
            info_owner=data_contract.info.owner,
            info_contact=data_contract.info.contact.dict() if data_contract.info.contact else None,
            servers=data_contract.servers,
            terms=data_contract.terms.model_dump() if data_contract.terms else None,
            models=data_contract.models,
            examples=[example.model_dump() for example in data_contract.examples] if data_contract.examples else None,
            service_levels=data_contract.service_levels.model_dump() if data_contract.service_levels else None,
            links={str(k): str(v) for k, v in data_contract.links.items()} if data_contract.links else None,
            tags=data_contract.tags,
        )
        db.add(db_data_contract)
        db.commit()
        db.refresh(db_data_contract)
        logger.info(f" ✅ Data contract created successfully: {db_data_contract.id}")
        return DataContract(**data_contract.model_dump())
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f" ❌ Failed to create data contract: {str(e)}")
        raise
    except Exception as e:
        logger.error(f" ❌ Unexpected error occurred while creating data contract: {str(e)}")
        raise
