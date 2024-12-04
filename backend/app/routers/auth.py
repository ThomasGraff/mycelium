import json
from datetime import timedelta
from typing import Any, Dict

import httpx
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPBearer
from passlib.context import CryptContext

from ..schemas.auth.routes.login import LoginInput, LoginResponse
from ..schemas.auth.routes.logout import LogoutResponse
from ..schemas.auth.routes.me import MeResponse
from ..schemas.auth.routes.register import RegisterInput, RegisterResponse
from ..utils.auth import (
    create_access_token,
    get_current_user_from_token,
    get_current_user_token,
    get_system_user_token,
)
from ..utils.config import settings
from ..utils.logger import get_logger

router = APIRouter(tags=["Auth"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

logger = get_logger(__name__)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Registers a new user in Authentik.",
    response_description="Successfully registered user",
    responses={
        201: {
            "content": {"application/json": {"example": {"message": " ✅ User registered successfully"}}},
        },
        400: {
            "description": "Invalid input",
            "content": {"application/json": {"example": {"detail": " ❌ Registration failed: Invalid input"}}},
        },
        500: {
            "description": "Internal server error",
            "content": {"application/json": {"example": {"detail": " ❌ Registration error: Internal server error"}}},
        },
    },
)
async def register(user_data: RegisterInput) -> RegisterResponse:
    """
    Registers a new user in Authentik.

    This endpoint accepts user registration data and creates a new user account
    in the Authentik authentication system using an API token.

    :param RegisterInput user_data: The user registration information
    :return RegisterResponse: Success message
    :raises HTTPException:
        - 400 Bad Request: If registration data is invalid
        - 500 Internal Server Error: If there's an unexpected error during registration
    """
    try:
        access_token, token_type = await get_system_user_token()
        async with httpx.AsyncClient() as client:
            request_data = user_data.model_dump(mode="json")
            response = await client.post(
                f"{settings.AUTHENTIK_URL}/api/v3/core/users/",
                json=request_data,
                headers={
                    "Authorization": f"{token_type} {access_token}",
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            logger.info(" ✅ User registered successfully")
            return RegisterResponse(message=" ✅ User registered successfully")

    except httpx.HTTPStatusError as e:
        logger.error(f" ❌ Registration failed: {e.response.text}")
        error_detail = " ❌ Registration failed"
        try:
            error_json = e.response.json()
            if isinstance(error_json, dict):
                error_detail = f" ❌ Registration failed: {error_json.get('detail', str(e))}"
        except json.JSONDecodeError:
            error_detail = f" ❌ Registration failed: {e.response.text}"
        raise HTTPException(status_code=e.response.status_code, detail=error_detail)
    except Exception as e:
        logger.error(f" ❌ Unexpected registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=" ❌ Registration failed: Internal server error",
        )


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticates a user against Authentik and returns access tokens.",
    response_description="Successfully authenticated user",
    responses={
        200: {
            "content": {
                "application/json": {"example": {"access_token": "token", "token_type": "bearer", "expires_in": 1800}}
            },
        },
        401: {
            "description": "Invalid credentials",
            "content": {"application/json": {"example": {"detail": " ❌ Invalid credentials"}}},
        },
        500: {
            "description": "Internal server error",
            "content": {"application/json": {"example": {"detail": " ❌ Login failed: Internal server error"}}},
        },
    },
)
async def login(response: Response, user_data: LoginInput) -> LoginResponse:
    """
    Authenticates a user against Authentik and returns access tokens.

    :param Response response: FastAPI response object for setting cookies
    :param LoginInput user_data: The user credentials for authentication
    :return LoginResponse: Access token and related information
    :raises HTTPException: If authentication fails
    """
    try:
        auth_result = await get_current_user_token(user_data.username, user_data.password, user_data.mfa_code)

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user_data.username,
                "authentik_token": auth_result["access_token"],
                "scope": auth_result.get("scope", ""),
            },
            expires_delta=access_token_expires,
        )

        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
        )

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    except httpx.HTTPStatusError as e:
        logger.error(f" ❌ Authentication failed: {e.response.text}")
        error_detail = " ❌ Invalid username or password"
        if e.response.status_code != 401:
            try:
                error_json = e.response.json()
                error_detail = f" ❌ Authentication failed: {error_json.get('detail', str(e))}"
            except json.JSONDecodeError:
                error_detail = f" ❌ Authentication failed: {e.response.text}"
        raise HTTPException(status_code=e.response.status_code, detail=error_detail)
    except Exception as e:
        logger.error(f" ❌ Unexpected authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=" ❌ Authentication failed: Internal server error",
        )


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Logs out the current user by clearing their access token cookie.",
    response_description="Successfully logged out user",
    responses={
        200: {
            "content": {"application/json": {"example": {"message": " ✅ Logged out successfully"}}},
        },
    },
)
async def logout(response: Response) -> LogoutResponse:
    """
    Logs out the current user.

    This endpoint clears the user's access token cookie, effectively logging them out.

    :param Response response: FastAPI response object for clearing cookies
    :return LogoutResponse: Success message
    """
    response.delete_cookie("access_token")
    return LogoutResponse(message=" ✅ Logged out successfully")


@router.get(
    "/me",
    response_model=MeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Retrieves information about the currently authenticated user.",
    response_description="Successfully retrieved user information",
    responses={
        200: {
            "content": {"application/json": {"example": {"user": {"sub": "username", "email": "user@example.com"}}}},
        },
        401: {
            "description": "Not authenticated",
            "content": {"application/json": {"example": {"detail": " ❌ Not authenticated"}}},
        },
    },
)
async def get_current_user(user: Dict[str, Any] = Depends(get_current_user_from_token)) -> MeResponse:
    """
    Retrieves information about the currently authenticated user.

    This endpoint extracts user information from the access token
    in the request cookies.

    :param Request request: FastAPI request object containing cookies
    :return MeResponse: Current user information
    :raises HTTPException:
        - 401 Unauthorized: If user is not authenticated or token is invalid
    """
    return MeResponse(user=user)
