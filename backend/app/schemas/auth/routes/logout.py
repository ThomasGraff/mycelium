from pydantic import BaseModel


class LogoutResponse(BaseModel):
    """Logout response model"""

    message: str
