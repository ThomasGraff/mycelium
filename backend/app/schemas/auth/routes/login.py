from typing import Optional

from pydantic import BaseModel

from ..objects.token import Token


class LoginInput(BaseModel):
    """Login request model"""

    username: str
    password: str
    mfa_code: Optional[str] = None


class LoginResponse(Token):
    """Login response model"""

    pass
