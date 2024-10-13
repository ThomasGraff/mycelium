import logging
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models.data_contracts import DataContract as DataContractModel
from ..schemas.data_contract_create import DataContractCreate
from ..schemas.data_contract_update import DataContractUpdate
from ..schemas.data_contracts import DataContract
from ..utils.config import settings
from ..utils.tools import db_to_pydantic_model, pydantic_to_db_model

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
        created_data_contract = DataContract.model_validate(data_contract.model_dump())
        db_data_contract = pydantic_to_db_model(created_data_contract)
        db.add(db_data_contract)
        db.commit()
        db.refresh(db_data_contract)
        logger.info(f" ✅ Data contract created successfully: {db_data_contract.id}")
        return created_data_contract
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f" ❌ Failed to create data contract: {str(e)}")
        raise
    except Exception as e:
        logger.error(f" ❌ Unexpected error occurred while creating data contract: {str(e)}")
        raise


def get_data_contract(db: Session, id: str) -> Optional[DataContract]:
    """
    Retrieves a data contract from the database by its ID.

    :param Session db: The database session.
    :param str id: The unique identifier of the data contract to retrieve.
    :return Optional[DataContract]: The retrieved data contract, or None if not found.
    :raises SQLAlchemyError: If there's an error during database operations.
    :raises Exception: If there's any other unexpected error.
    """
    try:
        db_data_contract = db.query(DataContractModel).filter(DataContractModel.id == id).first()
        if db_data_contract is None:
            logger.warning(f" ⚠️ Data contract not found: {id}")
            return None
        data_contract = db_to_pydantic_model(db_data_contract)
        logger.info(f" ✅ Data contract retrieved successfully: {id}")
        return data_contract
    except SQLAlchemyError as e:
        logger.error(f" ❌ Failed to retrieve data contract: {str(e)}")
        raise
    except Exception as e:
        logger.error(f" ❌ Unexpected error occurred while retrieving data contract: {str(e)}")
        raise


def update_data_contract(db: Session, id: str, data_contract_update: DataContractUpdate) -> Optional[DataContract]:
    """
    Updates an existing data contract in the database.

    :param Session db: The database session.
    :param str id: The unique identifier of the data contract to update.
    :param DataContractUpdate data_contract_update: The data contract update information.
    :return Optional[DataContract]: The updated data contract, or None if not found.
    :raises SQLAlchemyError: If there's an error during database operations.
    :raises Exception: If there's any other unexpected error.
    """
    try:
        db_data_contract = db.query(DataContractModel).filter(DataContractModel.id == id).first()
        if db_data_contract is None:
            logger.warning(f" ⚠️ Data contract not found for update: {id}")
            return None

        updated_data_contract = DataContract.model_validate(data_contract_update.model_dump(exclude_unset=True))
        updated_data_contract_db = pydantic_to_db_model(updated_data_contract)

        for key, value in updated_data_contract_db.__dict__.items():
            if hasattr(db_data_contract, key):
                setattr(db_data_contract, key, value)
            else:
                logger.warning(f" ⚠️ Attribute {key} not found in DataContractModel")
        db.commit()
        logger.info(f" ✅ Data contract updated successfully: {id}")
        return updated_data_contract
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f" ❌ Failed to update data contract: {str(e)}")
        raise
    except Exception as e:
        logger.error(f" ❌ Unexpected error occurred while updating data contract: {str(e)}")
        raise
