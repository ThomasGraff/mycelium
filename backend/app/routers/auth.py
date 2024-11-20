from datetime import timedelta

import httpx
from fastapi import APIRouter, HTTPException, Request, Response, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..schemas.auth.routes.login import LoginInput, LoginResponse
from ..schemas.auth.routes.logout import LogoutResponse
from ..schemas.auth.routes.me import MeResponse
from ..schemas.auth.routes.register import RegisterInput, RegisterResponse
from ..utils.auth import create_access_token, verify_authentik_credentials
from ..utils.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login", response_model=LoginResponse)
async def login(response: Response, user_data: LoginInput) -> LoginResponse:
    """Login endpoint"""
    try:
        # Verify credentials with Authentik
        auth_result = await verify_authentik_credentials(user_data.username, user_data.password, user_data.mfa_code)

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
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
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

        return LoginResponse(
            access_token=access_token, token_type="bearer", expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Login failed: {str(e)}")


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: RegisterInput) -> RegisterResponse:
    """Register new user in Authentik"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.AUTHENTIK_URL}/api/v3/core/users/",
                json={
                    "username": user_data.username,
                    "email": user_data.email,
                    "password": user_data.password,
                    "name": user_data.full_name,
                },
            )
            if response.status_code == 201:
                return RegisterResponse(message=" ✅ User registered successfully")
            raise HTTPException(status_code=response.status_code, detail=f" ❌ Registration failed: {response.text}")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Registration error: {str(e)}"
            )


@router.post("/logout", response_model=LogoutResponse)
async def logout(response: Response) -> LogoutResponse:
    """Logout user"""
    response.delete_cookie("access_token")
    return LogoutResponse(message=" ✅ Logged out successfully")


@router.get("/me", response_model=MeResponse)
async def get_current_user(request: Request) -> MeResponse:
    """Get current user info"""
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" ❌ Not authenticated")

        token = token.replace("Bearer ", "")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return MeResponse(user=payload)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" ❌ Invalid token")
