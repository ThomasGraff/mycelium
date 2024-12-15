"""Registration flow implementation."""

from typing import Any, Dict

from fastapi import HTTPException, status

from ...utils.logger import get_logger
from ..providers.authentik import AuthentikProvider

logger = get_logger(__name__)


async def register_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Register a new user in Authentik.

    :param Dict[str, Any] user_data: User registration data
    :return Dict[str, Any]: Created user data
    :raises HTTPException: If registration fails
    """
    provider = AuthentikProvider()
    try:
        result = await provider.create_user(user_data)
        logger.info(" ✅ User registered successfully")
        return result
    except HTTPException as e:
        logger.error(f" ❌ Registration failed: {e.detail}")
        raise
    except Exception as e:
        logger.error(f" ❌ Unexpected registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=" ❌ Registration failed: Internal server error",
        )
