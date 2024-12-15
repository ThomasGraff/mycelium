"""Security utilities for authentication."""

from typing import Optional

from fastapi import Cookie, Header
from fastapi.security import HTTPBearer
from passlib.context import CryptContext

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def get_token_from_auth_header(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """
    Extract token from Authorization header.

    :param Optional[str] authorization: Authorization header value
    :return Optional[str]: Extracted token or None
    """
    if authorization and authorization.startswith("Bearer "):
        return authorization.replace("Bearer ", "")
    return None


def get_token_from_cookie(access_token: Optional[str] = Cookie(None)) -> Optional[str]:
    """
    Extract token from cookie.

    :param Optional[str] access_token: Access token cookie value
    :return Optional[str]: Extracted token or None
    """
    if access_token and access_token.startswith("Bearer "):
        return access_token.replace("Bearer ", "")
    return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    :param str plain_password: Plain text password
    :param str hashed_password: Hashed password
    :return bool: True if password matches hash
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password.

    :param str password: Plain text password
    :return str: Hashed password
    """
    return pwd_context.hash(password)
