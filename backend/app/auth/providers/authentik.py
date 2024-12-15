"""Authentik authentication provider implementation."""

from typing import Any, Dict, Optional

import httpx
from fastapi import HTTPException, status

from ...utils.config import settings
from ...utils.logger import get_logger

logger = get_logger(__name__)


class AuthentikProvider:
    """Authentik authentication provider implementation."""

    def __init__(self) -> None:
        """Initialize the Authentik provider with configuration."""
        self.base_url = settings.AUTHENTIK_URL
        self.client_id = settings.AUTHENTIK_CLIENT_ID
        self.client_secret = settings.AUTHENTIK_CLIENT_SECRET
        self.flow_url = f"{self.base_url}/api/v3/flows/executor/default-authentication-flow/"
        self.session_cookie = None

    async def _make_request(
        self,
        method: str,
        url: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        client: Optional[httpx.AsyncClient] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to Authentik."""
        default_headers = {
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": (
                "application/json" if json else "application/x-www-form-urlencoded" if data else "application/json"
            ),
        }

        should_close = not client
        client = client or httpx.AsyncClient(follow_redirects=True)

        try:
            response = await client.request(
                method,
                url,
                json=json,
                data=data,
                headers={**default_headers, **(headers or {})},
                cookies={"authentik_session": self.session_cookie} if self.session_cookie else None,
            )

            if "authentik_session" in response.cookies:
                self.session_cookie = response.cookies["authentik_session"]

            try:
                response_data = response.json()
            except Exception:
                response_data = {}

            # Special handling for OAuth token errors
            if url.endswith("/token/") and response.status_code != 200:
                error_msg = response_data.get("error_description", response_data.get("detail", "Token request failed"))
                logger.error(f" ❌ OAuth token error: {error_msg}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f" ❌ {error_msg}",
                )

            if response.status_code in (401, 403):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=" ❌ Authentication failed",
                )
            elif response.status_code == 400:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f" ❌ {response_data.get('detail', 'Bad request')}",
                )
            elif response.status_code >= 500:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=" ❌ Authentication service temporarily unavailable",
                )

            response.raise_for_status()
            return response_data

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f" ❌ Request failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f" ❌ Request failed: {str(e)}",
            )
        finally:
            if should_close:
                await client.aclose()

    async def get_oauth_token(
        self,
        *,
        grant_type: str = "password",
        username: Optional[str] = None,
        password: Optional[str] = None,
        refresh_token: Optional[str] = None,
        scope: str = "openid email profile",
    ) -> Dict[str, Any]:
        """Get an OAuth token from Authentik."""
        try:
            if grant_type == "password":
                if not username or not password:
                    raise ValueError("Username and password required for password grant")

                # First get an authorization code
                auth_data = {
                    "client_id": self.client_id,
                    "response_type": "code",
                    "redirect_uri": f"{self.base_url}/application/o/callback/",
                    "scope": scope,
                }

                # Get the authorization code
                auth_response = await self._make_request(
                    "POST",
                    f"{self.base_url}/application/o/authorize/",
                    data=auth_data,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "application/json",
                    },
                )

                # Extract the authorization code from the redirect URL
                auth_code = None
                if auth_response.get("type") == "redirect":
                    redirect_url = auth_response.get("to", "")
                    if "code=" in redirect_url:
                        auth_code = redirect_url.split("code=")[1].split("&")[0]

                if not auth_code:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=" ❌ Failed to obtain authorization code",
                    )

                # Exchange the code for tokens
                token_data = {
                    "grant_type": "authorization_code",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": auth_code,
                    "redirect_uri": f"{self.base_url}/application/o/callback/",
                }

                result = await self._make_request(
                    "POST",
                    f"{self.base_url}/application/o/token/",
                    data=token_data,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "application/json",
                    },
                )
                logger.info(" ✅ Token obtained successfully")
                return result

            elif grant_type == "refresh_token":
                if not refresh_token:
                    raise ValueError("Refresh token required for refresh_token grant")

                refresh_data = {
                    "grant_type": "refresh_token",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                    "scope": scope,
                }

                result = await self._make_request(
                    "POST",
                    f"{self.base_url}/application/o/token/",
                    data=refresh_data,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "application/json",
                    },
                )
                logger.info(" ✅ Token refreshed successfully")
                return result

            else:
                # Client credentials flow
                data = {
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "scope": scope,
                }

                result = await self._make_request(
                    "POST",
                    f"{self.base_url}/application/o/token/",
                    data=data,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "application/json",
                    },
                )
                logger.info(" ✅ Client credentials token obtained successfully")
                return result

        except Exception as e:
            error_msg = str(e)
            if hasattr(e, "response"):
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get("error_description", error_data.get("detail", str(e)))
                except Exception:
                    error_msg = e.response.text or str(e)

            logger.error(f" ❌ Token exchange failed: {error_msg}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f" ❌ Token exchange failed: {error_msg}",
            )

    async def verify_user_token(self, token: str) -> Dict[str, Any]:
        """Verify a user token with Authentik."""
        return await self._make_request(
            "GET",
            f"{self.base_url}/api/v3/core/users/me/",
            headers={"Authorization": f"Bearer {token}"},
        )
