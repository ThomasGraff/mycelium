from pydantic import BaseModel, EmailStr
from typing import Optional

class SupabaseAuthBase(BaseModel):
    email: EmailStr
    password: str

class SupabaseSignUp(SupabaseAuthBase):
    full_name: Optional[str] = None

class SupabaseSignIn(SupabaseAuthBase):
    pass

class SupabaseAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str 