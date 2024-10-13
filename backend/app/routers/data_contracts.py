from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import data_contracts
from ..database.manager import db_manager
from ..schemas.data_contract_create import (
    DataContractCreate,
    DataContractCreateResponse,
)

router = APIRouter()


@router.post(
    "/",
    response_model=DataContractCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new data contract",
    description="Creates a new data contract and stores it in the database.",
    response_description="Successfully created data contract",
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": DataContractCreateResponse.model_config["json_schema_extra"]["example"]
                }
            },
        },
        400: {
            "description": "Invalid input",
            "content": {"application/json": {"example": {"detail": " ❌ Invalid data contract schema"}}},
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": " ❌ Failed to create data contract: Internal server error"}
                }
            },
        },
    },
    tags=["Data Contracts"],
)
async def create_data_contract(
    data_contract: DataContractCreate,
    db: Session = Depends(db_manager.get_db),
) -> DataContractCreateResponse:
    """
    Creates a new data contract and stores it in the database.

    This endpoint accepts a DataContractCreate object, validates it, and attempts to create
    a new data contract in the database. If successful, it returns the created contract.
    If an error occurs during the process, it raises an appropriate HTTP exception.

    :param DataContractCreate data_contract: The data contract to be created, validated against the DataContractCreate model.
    :param Session db: The database session, automatically provided by FastAPI's dependency injection.
    :return DataContractCreateResponse: A response containing a success message and the created data contract.
    :raises HTTPException:
        - 400 Bad Request: If the input data is invalid.
        - 500 Internal Server Error: If there's an unexpected error during contract creation.
    """
    try:
        created_contract = data_contracts.create_data_contract(db, data_contract)
        return DataContractCreateResponse(message=" ✅ Data contract created successfully", data=created_contract)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f" ❌ Invalid data contract schema: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Failed to create data contract: {str(e)}"
        )
