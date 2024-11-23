from typing import Dict, List, Optional
from fastapi import HTTPException, status
from .client import supabase_client

class SupabaseStorage:
    TABLE_NAME = "data_contracts"

    @staticmethod
    async def create_data_contract(data: Dict) -> Dict:
        try:
            response = supabase_client.table(SupabaseStorage.TABLE_NAME).insert(data).execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create data contract: {str(e)}"
            )

    @staticmethod
    async def get_data_contract(id: str) -> Optional[Dict]:
        try:
            response = supabase_client.table(SupabaseStorage.TABLE_NAME).select("*").eq("id", id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to retrieve data contract: {str(e)}"
            )

    @staticmethod
    async def list_data_contracts() -> List[Dict]:
        try:
            response = supabase_client.table(SupabaseStorage.TABLE_NAME).select("*").execute()
            return response.data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to list data contracts: {str(e)}"
            ) 