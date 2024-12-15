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
        # Use the default authentication flow
        self.flow_url = f"{self.base_url}/api/v3/flows/executor/default-authentication-flow/"
        self.session_cookie = None

        # Log provider configuration
        logger.info(" 💡 Authentik provider configuration:")
        logger.info(f" 💡 Base URL: {self.base_url}")
        logger.info(f" 💡 Client ID: {self.client_id}")
        logger.info(f" 💡 Flow URL: {self.flow_url}")
        logger.info(" 💡 Using default authentication flow")
        # Don't log the client secret for security reasons

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
        """
        Make an HTTP request to Authentik.

        :param str method: HTTP method to use
        :param str url: URL to request
        :param Optional[Dict[str, Any]] json: JSON data to send
        :param Optional[Dict[str, Any]] data: Form data to send
        :param Optional[Dict[str, str]] headers: Headers to include
        :param Optional[httpx.AsyncClient] client: HTTP client to use
        :return Dict[str, Any]: Response data
        :raises HTTPException: If the request fails
        """
        default_headers = {
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        }
        if json:
            default_headers["Content-Type"] = "application/json"
        elif data:
            default_headers["Content-Type"] = "application/x-www-form-urlencoded"

        headers = {**default_headers, **(headers or {})}

        should_close = False
        if not client:
            client = httpx.AsyncClient(follow_redirects=True)
            should_close = True

        try:
            logger.debug(f" 💡 Making {method} request to {url}")
            if json:
                logger.debug(f" 💡 Request JSON: {json}")
            if data:
                logger.debug(f" 💡 Request data: {data}")

            # Include session cookie if available
            cookies = {}
            if self.session_cookie:
                cookies["authentik_session"] = self.session_cookie

            response = await client.request(method, url, json=json, data=data, headers=headers, cookies=cookies)

            # Store session cookie if present
            if "authentik_session" in response.cookies:
                self.session_cookie = response.cookies["authentik_session"]
                logger.debug(" 💡 Stored session cookie")

            # Log response details
            logger.debug(f" 💡 Response status: {response.status_code}")
            try:
                response_data = response.json()
                logger.debug(f" 💡 Response data: {response_data}")
            except Exception:
                logger.debug(f" 💡 Raw response: {response.text}")
                response_data = {}

            # Check for specific error responses
            if response.status_code == 401:
                logger.error(" ❌ Authentication failed")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=" ❌ Authentication failed",
                )
            elif response.status_code == 400:
                error_detail = response_data.get("detail", "Bad request")
                logger.error(f" ❌ Bad request: {error_detail}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f" ❌ {error_detail}",
                )

            response.raise_for_status()
            return response_data

        except httpx.HTTPError as e:
            logger.error(f" ❌ Authentik request failed: {str(e)}")
            if hasattr(e, "response"):
                try:
                    error_data = e.response.json()
                    error_detail = error_data.get("detail", str(e))
                except Exception:
                    error_detail = e.response.text or str(e)
            else:
                error_detail = str(e)

            if e.response and e.response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f" ❌ Authentication failed: {error_detail}",
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f" ❌ Authentik request failed: {error_detail}",
            )
        finally:
            if should_close:
                await client.aclose()

    async def get_oauth_token(
        self,
        *,
        grant_type: str = "client_credentials",
        username: Optional[str] = None,
        password: Optional[str] = None,
        refresh_token: Optional[str] = None,
        scope: str = "openid email profile",
    ) -> Dict[str, Any]:
        """
        Get an OAuth token from Authentik.

        :param str grant_type: OAuth grant type to use
        :param Optional[str] username: Username for password grant
        :param Optional[str] password: Password for password grant
        :param Optional[str] refresh_token: Refresh token for refresh grant
        :param str scope: OAuth scopes to request
        :return Dict[str, Any]: Token response data
        :raises HTTPException: If token request fails
        """
        data = {
            "grant_type": grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": scope,
        }

        if grant_type == "password":
            if not username or not password:
                raise ValueError("Username and password required for password grant")
            data.update({"username": username, "password": password})
        elif grant_type == "refresh_token":
            if not refresh_token:
                raise ValueError("Refresh token required for refresh_token grant")
            data["refresh_token"] = refresh_token

        logger.debug(f" 💡 Requesting OAuth token with grant type: {grant_type}")
        try:
            result = await self._make_request(
                "POST",
                f"{self.base_url}/application/o/token/",
                data=data,
            )
            logger.debug(" ✅ OAuth token obtained successfully")
            return result
        except Exception as e:
            logger.error(f" ❌ Failed to obtain OAuth token: {str(e)}")
            raise

    async def verify_user_token(self, token: str) -> Dict[str, Any]:
        """
        Verify a user token with Authentik.

        :param str token: Token to verify
        :return Dict[str, Any]: User data if token is valid
        :raises HTTPException: If token is invalid
        """
        return await self._make_request(
            "GET",
            f"{self.base_url}/api/v3/core/users/me/",
            headers={"Authorization": f"Bearer {token}"},
        )

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user in Authentik.

        :param Dict[str, Any] user_data: User data to create
        :return Dict[str, Any]: Created user data
        :raises HTTPException: If user creation fails
        """
        token_data = await self.get_oauth_token(scope="openid email profile goauthentik.io/api")
        return await self._make_request(
            "POST",
            f"{self.base_url}/api/v3/core/users/",
            json=user_data,
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )

    async def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the OAuth provider configuration."""
        try:
            # First get a token with admin scope
            token_data = await self.get_oauth_token(scope="openid email profile goauthentik.io/api")

            # Get all OAuth providers
            result = await self._make_request(
                "GET",
                f"{self.base_url}/api/v3/providers/oauth2/",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            # Find our provider by client ID
            our_provider = None
            for provider in result.get("results", []):
                if provider.get("client_id") == self.client_id:
                    our_provider = provider
                    break

            if our_provider:
                logger.info(" 💡 Found our OAuth provider configuration:")
                logger.info(f" 💡 Name: {our_provider.get('name')}")
                logger.info(f" 💡 Client ID: {our_provider.get('client_id')}")
                logger.info(f" 💡 Client Type: {our_provider.get('client_type')}")
                logger.info(f" 💡 Authorization Flow: {our_provider.get('authorization_flow')}")
                logger.info(f" 💡 Authentication Flow: {our_provider.get('authentication_flow')}")
                logger.info(f" 💡 Grant Types: {our_provider.get('grant_types', [])}")
                logger.info(f" 💡 Property Mappings: {our_provider.get('property_mappings', [])}")
                logger.info(f" 💡 Redirect URIs: {our_provider.get('redirect_uris', [])}")
                logger.info(f" 💡 Access Token Validity: {our_provider.get('access_token_validity')}")
                logger.info(f" 💡 Refresh Token Validity: {our_provider.get('refresh_token_validity')}")
                logger.info(f" 💡 Include Claims in ID Token: {our_provider.get('include_claims_in_id_token')}")
                logger.info(f" 💡 Sub Mode: {our_provider.get('sub_mode')}")
                logger.info(f" 💡 Issuer Mode: {our_provider.get('issuer_mode')}")
            else:
                logger.warning(f" ⚠️ Could not find OAuth provider with client ID: {self.client_id}")
                logger.info(" 💡 Available providers:")
                for provider in result.get("results", []):
                    logger.info(f" 💡 - {provider.get('name')} (client_id: {provider.get('client_id')})")

            return our_provider or {}
        except Exception as e:
            logger.error(f" ❌ Failed to get provider info: {str(e)}")
            return {}

    async def get_available_flows(self) -> Dict[str, Any]:
        """Get information about available authentication flows."""
        try:
            result = await self._make_request(
                "GET",
                f"{self.base_url}/api/v3/flows/instances/",
                headers={"Authorization": f"Bearer {(await self.get_oauth_token())['access_token']}"},
            )
            logger.info(" 💡 Available authentication flows:")
            for flow in result.get("results", []):
                logger.info(f" 💡 Flow: {flow.get('name')} (slug: {flow.get('slug')})")
            return result
        except Exception as e:
            logger.error(f" ❌ Failed to get flows: {str(e)}")
            return {}
