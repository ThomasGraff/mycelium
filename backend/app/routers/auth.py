"""Authentication router."""

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Response, status

from ..auth import authenticate_user, get_current_user_from_token, register_user
from ..auth.utils.cookies import clear_auth_cookies, set_auth_cookies
from ..schemas.auth.routes.login import LoginInput, LoginResponse
from ..schemas.auth.routes.logout import LogoutResponse
from ..schemas.auth.routes.me import MeResponse
from ..schemas.auth.routes.register import RegisterInput, RegisterResponse
from ..utils.logger import get_logger

router = APIRouter(tags=["Auth"])
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
    in the Authentik authentication system.

    :param RegisterInput user_data: The user registration information
    :return RegisterResponse: Success message
    :raises HTTPException:
        - 400 Bad Request: If registration data is invalid
        - 500 Internal Server Error: If there's an unexpected error during registration
    """
    try:
        await register_user(user_data.model_dump(mode="json"))
        return RegisterResponse(message=" ✅ User registered successfully")
    except HTTPException:
        raise
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
    description="Authenticates a user using Authentik's authentication flow and returns access tokens.",
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
    Authenticates a user using Authentik's authentication flow and returns access tokens.

    :param Response response: FastAPI response object for setting cookies
    :param LoginInput user_data: The user credentials for authentication
    :return LoginResponse: Access token and related information
    :raises HTTPException: If authentication fails
    """
    try:
        auth_result = await authenticate_user(user_data.username, user_data.password, user_data.mfa_code)
        set_auth_cookies(response, auth_result)
        return LoginResponse(
            access_token=auth_result["access_token"],
            token_type="bearer",
            expires_in=3600,  # 1 hour, matching Authentik's default
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f" ❌ Unexpected login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f" ❌ Login failed: {str(e)}",
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
    clear_auth_cookies(response)
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

    :param Dict[str, Any] user: Current user information from token
    :return MeResponse: Current user information
    :raises HTTPException:
        - 401 Unauthorized: If user is not authenticated or token is invalid
    """
    return MeResponse(user=user)
