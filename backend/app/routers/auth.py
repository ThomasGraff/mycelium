from os import getenv
from typing import Any, Dict

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

# Environment configuration
AUTHENTIK_HOST = getenv("AUTHENTIK_HOST", "https://auth.example.com")
AUTHENTIK_CLIENT_ID = getenv("AUTHENTIK_CLIENT_ID")
AUTHENTIK_CLIENT_SECRET = getenv("AUTHENTIK_CLIENT_SECRET")


class AuthResponse(BaseModel):
    """
    Standard response model for authentication endpoints
    """

    message: str = Field(
        ..., example=" ✅ Authentication successful", description="Status message of the authentication operation"
    )
    data: Dict[str, Any] | None = Field(
        default=None,
        example={"user": {"email": "user@example.com", "name": "John Doe"}},
        description="Response data containing user information",
    )


# Configure OAuth client
oauth = OAuth()
oauth.register(
    name="authentik",
    server_metadata_url=f"{AUTHENTIK_HOST}/.well-known/openid-configuration",
    client_id=AUTHENTIK_CLIENT_ID,
    client_secret=AUTHENTIK_CLIENT_SECRET,
    authorize_url=f"{AUTHENTIK_HOST}/application/o/authorize/",
    access_token_url=f"{AUTHENTIK_HOST}/application/o/token/",
    api_base_url=f"{AUTHENTIK_HOST}/application/o/userinfo/",
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        401: {
            "description": "Authentication failed",
            "content": {"application/json": {"example": {"detail": " ❌ Authentication failed"}}},
        },
        500: {
            "description": "Internal server error",
            "content": {"application/json": {"example": {"detail": " ❌ Internal server error"}}},
        },
    },
)


@router.get(
    "/login",
    summary="Initiate OAuth2 login",
    description="Initiates the OAuth2 authentication flow with Authentik",
    response_description="Redirects to Authentik login page",
)
async def login(request: Request) -> RedirectResponse:
    """
    Initiates the OAuth2 authentication flow with Authentik.

    :param Request request: The incoming request object
    :return RedirectResponse: Redirect to Authentik login page
    """
    redirect_uri = request.url_for("auth_callback")
    return await oauth.authentik.authorize_redirect(request, redirect_uri)


@router.get(
    "/callback",
    response_model=AuthResponse,
    summary="Handle OAuth2 callback",
    description="Processes the OAuth2 callback from Authentik after successful authentication",
)
async def auth_callback(request: Request) -> RedirectResponse:
    """
    Handles the OAuth2 callback from Authentik after successful authentication.

    :param Request request: The incoming request object containing the authentication response
    :return RedirectResponse: Redirect to dashboard with authentication cookie
    :raises HTTPException: If authentication fails
    """
    try:
        token = await oauth.authentik.authorize_access_token(request)
        await oauth.authentik.parse_id_token(request, token)

        response = RedirectResponse(url="/dashboard")
        response.set_cookie(key="auth_token", value=token["access_token"], httponly=True, secure=True, samesite="lax")

        return response

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f" ❌ Authentication failed: {str(e)}")


@router.get(
    "/logout",
    response_model=AuthResponse,
    summary="Logout user",
    description="Logs out the current user by clearing their authentication token",
)
async def logout(request: Request) -> RedirectResponse:
    """
    Logs out the current user by clearing their authentication token.

    :param Request request: The incoming request object
    :return RedirectResponse: Redirect to login page
    """
    response = RedirectResponse(url="/login")
    response.delete_cookie("auth_token")
    return response


@router.get(
    "/me",
    response_model=AuthResponse,
    summary="Get current user",
    description="Retrieves information about the currently authenticated user",
)
async def get_current_user(request: Request) -> AuthResponse:
    """
    Retrieves information about the currently authenticated user.

    :param Request request: The incoming request object
    :return AuthResponse: The user information
    :raises HTTPException: If user is not authenticated or token is invalid
    """
    auth_token = request.cookies.get("auth_token")

    if not auth_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" ❌ Not authenticated")

    try:
        user_info = await oauth.authentik.parse_id_token(auth_token)
        return AuthResponse(message=" ✅ User information retrieved successfully", data={"user": user_info})

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" ❌ Invalid token")
