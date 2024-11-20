from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import httpx
from app.utils.config import settings
from fastapi import HTTPException, status
from jose import jwt


async def verify_authentik_credentials(username: str, password: str, mfa_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Verify credentials against Authentik

    :param str username: Username to verify
    :param str password: Password to verify
    :param Optional[str] mfa_code: MFA code if required
    :return Dict[str, Any]: Authentik response data
    :raises HTTPException: If authentication fails
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.AUTHENTIK_URL}/api/v3/core/auth/login/",
                json={"username": username, "password": password, "mfa_code": mfa_code},
            )
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" ❌ Invalid credentials")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Authentication error: {str(e)}"
            )


def create_access_token(data: Dict[str, Any], expires_delta: timedelta) -> str:
    """
    Create JWT access token

    :param Dict[str, Any] data: Data to encode in the token
    :param timedelta expires_delta: Token expiration time
    :return str: Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
