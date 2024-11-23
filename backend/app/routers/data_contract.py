from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..schemas.data_contract.routes.data_contract_create import DataContractCreate, DataContractCreateResponse
from ..schemas.data_contract.routes.data_contract_get import DataContractGetResponse
from ..schemas.data_contract.routes.data_contract_list import DataContractListResponse
from ..supabase.storage import SupabaseStorage
from ..middleware.auth import get_current_user

router = APIRouter(tags=["Data Contracts"])

@router.post(
    "/",
    response_model=DataContractCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_data_contract(
    data_contract: DataContractCreate,
    current_user = Depends(get_current_user)
) -> DataContractCreateResponse:
    """Create a new data contract."""
    try:
        data = data_contract.model_dump()
        data["user_id"] = current_user["id"]
        created_contract = await SupabaseStorage.create_data_contract(data)
        return DataContractCreateResponse(
            message="Data contract created successfully",
            data=created_contract
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/{id}",
    response_model=DataContractGetResponse
)
async def get_data_contract(
    id: str,
    current_user = Depends(get_current_user)
) -> DataContractGetResponse:
    """Retrieve a specific data contract."""
    try:
        contract = await SupabaseStorage.get_data_contract(id)
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data contract not found"
            )
        return DataContractGetResponse(
            message="Data contract retrieved successfully",
            data=contract
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=DataContractListResponse
)
async def list_data_contracts(
    current_user = Depends(get_current_user)
) -> DataContractListResponse:
    """List all data contracts for the current user."""
    try:
        contracts = await SupabaseStorage.list_data_contracts()
        return DataContractListResponse(
            message="Data contracts retrieved successfully",
            data=contracts
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
