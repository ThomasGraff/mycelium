from typing import Dict, Optional
from fastapi import HTTPException, status
from .client import supabase_client

class SupabaseAuth:
    @staticmethod
    async def sign_up(email: str, password: str) -> Dict:
        try:
            response = supabase_client.auth.sign_up({
                "email": email,
                "password": password
            })
            return response.dict()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to register: {str(e)}"
            )

    @staticmethod
    async def sign_in(email: str, password: str) -> Dict:
        try:
            response = supabase_client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return response.dict()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Failed to authenticate: {str(e)}"
            )

    @staticmethod
    async def sign_out(access_token: str) -> None:
        try:
            supabase_client.auth.sign_out()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to sign out: {str(e)}"
            ) 