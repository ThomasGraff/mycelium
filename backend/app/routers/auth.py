from datetime import datetime, timedelta
from os import getenv
from typing import Any, Dict, Optional

import httpx
from fastapi import APIRouter, HTTPException, Request, Response, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Environment variables
SECRET_KEY = getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
AUTHENTIK_URL = getenv("AUTHENTIK_URL", "https://auth.example.com")
AUTHENTIK_CLIENT_ID = getenv("AUTHENTIK_CLIENT_ID", "")
AUTHENTIK_CLIENT_SECRET = getenv("AUTHENTIK_CLIENT_SECRET", "")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    """Token response model"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserLogin(BaseModel):
    """User login request model"""

    username: str
    password: str
    mfa_code: Optional[str] = None


class UserRegister(BaseModel):
    """User registration request model"""

    email: EmailStr
    username: str
    password: str
    full_name: str


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
                f"{AUTHENTIK_URL}/api/v3/core/auth/login/",
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
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login", response_model=Token)
async def login(response: Response, user_data: UserLogin) -> Token:
    """Login endpoint"""
    try:
        # Verify credentials with Authentik
        auth_result = await verify_authentik_credentials(user_data.username, user_data.password, user_data.mfa_code)

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_data.username, **auth_result["user"]}, expires_delta=access_token_expires
        )

        # Set HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

        return Token(access_token=access_token, token_type="bearer", expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Login failed: {str(e)}")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister) -> Dict[str, str]:
    """Register new user in Authentik"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTHENTIK_URL}/api/v3/core/users/",
                json={
                    "username": user_data.username,
                    "email": user_data.email,
                    "password": user_data.password,
                    "name": user_data.full_name,
                },
            )
            if response.status_code == 201:
                return {"message": " ✅ User registered successfully"}
            raise HTTPException(status_code=response.status_code, detail=f" ❌ Registration failed: {response.text}")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Registration error: {str(e)}"
            )


@router.post("/logout")
async def logout(response: Response) -> Dict[str, str]:
    """Logout user"""
    response.delete_cookie("access_token")
    return {"message": " ✅ Logged out successfully"}


@router.get("/me")
async def get_current_user(request: Request) -> Dict[str, Any]:
    """Get current user info"""
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" ❌ Not authenticated")

        token = token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user": payload}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" ❌ Invalid token")
