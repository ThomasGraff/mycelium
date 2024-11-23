from fastapi import APIRouter, Depends, HTTPException, Response, status
from ..schemas.auth.routes.supabase_auth import (
    SupabaseSignUp,
    SupabaseSignIn,
    SupabaseAuthResponse
)
from ..supabase.auth import SupabaseAuth

router = APIRouter(tags=["Authentication"])

@router.post(
    "/register",
    response_model=SupabaseAuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(user_data: SupabaseSignUp) -> SupabaseAuthResponse:
    """Register a new user using Supabase authentication."""
    try:
        auth_response = await SupabaseAuth.sign_up(
            email=user_data.email,
            password=user_data.password
        )
        return SupabaseAuthResponse(
            access_token=auth_response["access_token"],
            user_id=auth_response["user"]["id"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post(
    "/login",
    response_model=SupabaseAuthResponse
)
async def login(user_data: SupabaseSignIn) -> SupabaseAuthResponse:
    """Authenticate a user using Supabase."""
    try:
        auth_response = await SupabaseAuth.sign_in(
            email=user_data.email,
            password=user_data.password
        )
        return SupabaseAuthResponse(
            access_token=auth_response["access_token"],
            user_id=auth_response["user"]["id"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/logout")
async def logout(response: Response) -> dict:
    """Log out the current user."""
    try:
        await SupabaseAuth.sign_out()
        response.delete_cookie("access_token")
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
