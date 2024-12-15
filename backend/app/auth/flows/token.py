"""Token management implementation."""

from typing import Any, Dict, Optional, Tuple

from fastapi import Cookie, Header, HTTPException, Request, status

from ...utils.logger import get_logger
from ..providers.authentik import AuthentikProvider

logger = get_logger(__name__)


async def get_system_user_token() -> Tuple[str, str]:
    """
    Get a system user access token from Authentik using OAuth2 client credentials flow.
    This generates a short-lived token with specific scopes for user management.

    :return Tuple[str, str]: A tuple containing (access_token, token_type)
    :raises HTTPException: If the token request fails
    """
    provider = AuthentikProvider()
    try:
        result = await provider.get_oauth_token(
            scope="openid email profile goauthentik.io/api goauthentik.io/api/v3 goauthentik.io/api/users"
        )
        return result["access_token"], result["token_type"]
    except Exception as e:
        logger.error(f" ❌ Failed to get system user token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=" ❌ Failed to get system access token",
        )


async def get_current_user_from_token(
    request: Request,
    authorization: Optional[str] = Header(None),
    access_token: Optional[str] = Cookie(None),
) -> Dict[str, Any]:
    """
    Get current user information from their access token.

    :param Request request: The FastAPI request object
    :param Optional[str] authorization: Optional Authorization header
    :param Optional[str] access_token: Optional access token cookie
    :return Dict[str, Any]: User information
    :raises HTTPException: If token is invalid or missing
    """
    token = None

    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    elif access_token and access_token.startswith("Bearer "):
        token = access_token.replace("Bearer ", "")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" ❌ Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    provider = AuthentikProvider()
    try:
        return await provider.verify_user_token(token)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f" ❌ Error verifying token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" ❌ Failed to verify token",
            headers={"WWW-Authenticate": "Bearer"},
        )
