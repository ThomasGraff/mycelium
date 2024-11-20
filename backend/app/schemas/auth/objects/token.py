from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Base token object model"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
