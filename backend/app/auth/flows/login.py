"""Login flow implementation."""

from typing import Any, Dict, Optional

import httpx
from fastapi import HTTPException, status

from ...utils.logger import get_logger
from ..providers.authentik import AuthentikProvider

logger = get_logger(__name__)


async def authenticate_user(username: str, password: str, mfa_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Authenticate a user through Authentik's authentication flow.

    :param str username: Username to authenticate
    :param str password: Password to verify
    :param Optional[str] mfa_code: Optional MFA code
    :return Dict[str, Any]: Authentication result with tokens
    :raises HTTPException: If authentication fails
    """
    provider = AuthentikProvider()

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            flow_result = await _execute_authentication_flow(client, provider, username, password, mfa_code)
            logger.info(f" 💡 Final flow state: {flow_result}")

            # Check various success conditions
            is_oauth_redirect = flow_result.get("type") == "redirect" and flow_result.get("to", "").startswith(
                "/application/o/"
            )
            is_success = flow_result.get("status") == "success"
            is_flow_complete = flow_result.get("flow_info", {}).get("flow_complete", False)
            is_root_redirect = flow_result.get("component") == "xak-flow-redirect" and flow_result.get("to") == "/"

            if is_oauth_redirect or is_success or is_flow_complete or is_root_redirect:
                try:
                    return await provider.get_oauth_token(
                        grant_type="password",
                        username=username,
                        password=password,
                    )
                except Exception as e:
                    logger.error(f" ❌ Token exchange failed: {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=" ❌ Authentication failed: Token exchange failed",
                    )

            # Log the reason for failure
            logger.error(" ❌ Authentication failed: Flow did not complete successfully")
            logger.error(f" ❌ Component: {flow_result.get('component')}")
            logger.error(f" ❌ Redirect to: {flow_result.get('to')}")
            logger.error(f" ❌ Flow type: {flow_result.get('type')}")
            logger.error(f" ❌ Flow status: {flow_result.get('status')}")
            logger.error(f" ❌ Flow info: {flow_result.get('flow_info')}")

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=" ❌ Authentication failed: Invalid credentials",
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f" ❌ Authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f" ❌ Authentication error: {str(e)}",
            )


async def _execute_authentication_flow(
    client: httpx.AsyncClient,
    provider: AuthentikProvider,
    username: str,
    password: str,
    mfa_code: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute the Authentik authentication flow through its various stages."""
    flow_result = await provider._make_request("GET", provider.flow_url, client=client)
    logger.info(f" 💡 Initial flow state: {flow_result}")

    # Handle identification stage
    flow_result = await _handle_identification_stage(client, provider, flow_result, username)
    logger.info(f" 💡 After identification: {flow_result}")

    # Handle password stage if needed
    if flow_result.get("component") == "ak-stage-password":
        flow_result = await _handle_password_stage(client, provider, password, flow_result)
        logger.info(f" 💡 After password: {flow_result}")

    # Handle MFA stage if needed
    if flow_result.get("component") == "ak-stage-authenticator-validate":
        if not mfa_code:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=" ❌ MFA code required",
                headers={"X-MFA-Required": "true"},
            )
        flow_result = await provider._make_request(
            "POST",
            provider.flow_url,
            json={"component": "ak-stage-authenticator-validate", "code": mfa_code},
            client=client,
        )
        logger.info(f" 💡 After MFA: {flow_result}")

    # Follow redirects until we get a final result
    max_redirects = 5
    while max_redirects > 0 and flow_result.get("type") == "redirect":
        redirect_url = flow_result.get("to", "")
        if not redirect_url.startswith("http"):
            redirect_url = f"{provider.base_url}{redirect_url}"

        logger.info(f" 💡 Following redirect to: {redirect_url}")

        # If we get an OAuth redirect, we're done
        if redirect_url.startswith(f"{provider.base_url}/application/o/"):
            logger.info(" 💡 Found OAuth redirect, completing flow")
            return flow_result

        flow_result = await provider._make_request("GET", redirect_url, client=client)
        logger.info(f" 💡 After redirect: {flow_result}")
        max_redirects -= 1

    return flow_result


async def _handle_identification_stage(
    client: httpx.AsyncClient,
    provider: AuthentikProvider,
    flow_data: Dict[str, Any],
    username: str,
) -> Dict[str, Any]:
    """Handle the identification stage of the authentication flow."""
    component = flow_data.get("component", "")
    if not component:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=" ❌ Invalid flow state",
        )

    payload = {
        "component": component,
        "uid_field": username,
    }
    if flow_data.get("session", {}).get("uid"):
        payload["session"] = flow_data["session"]["uid"]

    return await provider._make_request(
        "POST",
        provider.flow_url,
        json=payload,
        client=client,
    )


async def _handle_password_stage(
    client: httpx.AsyncClient,
    provider: AuthentikProvider,
    password: str,
    flow_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Handle the password stage of the authentication flow."""
    try:
        payload = {
            "component": "ak-stage-password",
            "password": password,
        }
        if flow_data.get("session", {}).get("uid"):
            payload["session"] = flow_data["session"]["uid"]
        if flow_data.get("pending_user"):
            payload["pending_user"] = flow_data["pending_user"]

        result = await provider._make_request(
            "POST",
            provider.flow_url,
            json=payload,
            client=client,
        )

        if result.get("response_errors", {}).get("password"):
            errors = result["response_errors"]["password"]
            error_msg = errors[0].get("string", "Invalid password") if errors else "Invalid password"
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f" ❌ {error_msg}",
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f" ❌ Password stage failed: {str(e)}",
        )
