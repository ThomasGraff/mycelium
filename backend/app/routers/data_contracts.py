from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import data_contracts
from ..database.manager import db_manager
from ..schemas.data_contract_create import (
    DataContractCreate,
    DataContractCreateResponse,
)
from ..schemas.data_contract_get import DataContractGetResponse

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


@router.get(
    "/{id}",
    response_model=DataContractGetResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a data contract",
    description="Retrieves a data contract from the database by its ID.",
    response_description="Successfully retrieved data contract",
    responses={
        200: {
            "content": {
                "application/json": {"example": DataContractGetResponse.model_config["json_schema_extra"]["example"]}
            },
        },
        404: {
            "description": "Data contract not found",
            "content": {"application/json": {"example": {"detail": " ❌ Data contract not found"}}},
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": " ❌ Failed to retrieve data contract: Internal server error"}
                }
            },
        },
    },
    tags=["Data Contracts"],
)
async def get_data_contract(
    id: str = "urn:datacontract:checkout:orders-latest",
    db: Session = Depends(db_manager.get_db),
) -> DataContractGetResponse:
    """
    Retrieves a data contract from the database by its ID.

    This endpoint accepts a data contract ID, attempts to retrieve the corresponding
    data contract from the database. If successful, it returns the retrieved contract.
    If the contract is not found or an error occurs, it raises an appropriate HTTP exception.

    :param str id: The unique identifier of the data contract to retrieve. Example: "urn:datacontract:checkout:orders-latest"
    :param Session db: The database session, automatically provided by FastAPI's dependency injection.
    :return DataContractGetResponse: A response containing a success message and the retrieved data contract.
    :raises HTTPException:
        - 404 Not Found: If the data contract with the given ID is not found.
        - 500 Internal Server Error: If there's an unexpected error during contract retrieval.
    """
    try:
        retrieved_contract = data_contracts.get_data_contract(db, id)
        if retrieved_contract is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" ❌ Data contract not found: {id}")
        return DataContractGetResponse(message=" ✅ Data contract retrieved successfully", data=retrieved_contract)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Failed to retrieve data contract: {str(e)}"
        )
