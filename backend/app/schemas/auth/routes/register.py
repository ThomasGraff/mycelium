from pydantic import BaseModel, EmailStr


class RegisterInput(BaseModel):
    """Register request model"""

    email: EmailStr
    username: str
    password: str
    full_name: str


class RegisterResponse(BaseModel):
    """Register response model"""

    message: str
