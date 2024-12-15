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

    # Get available flows
    try:
        await provider.get_available_flows()
    except Exception as e:
        logger.warning(f" ⚠️ Could not fetch available flows: {str(e)}")

    # Get provider configuration
    try:
        provider_info = await provider.get_provider_info()
        logger.info(" 💡 Using OAuth provider configuration:")
        logger.info(f" 💡 Authorization flow: {provider_info.get('authorization_flow')}")
        logger.info(f" 💡 Authentication flow: {provider_info.get('authentication_flow')}")
        logger.info(f" 💡 Grant types: {provider_info.get('grant_types', [])}")
        logger.info(f" 💡 Property mappings: {provider_info.get('property_mappings', [])}")
    except Exception as e:
        logger.warning(f" ⚠️ Could not fetch provider info: {str(e)}")

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            logger.debug(f" 💡 Starting authentication for user: {username}")
            flow_result = await _execute_authentication_flow(client, provider, username, password, mfa_code)

            # Check if we have a successful OAuth redirect
            if flow_result.get("type") == "redirect" and flow_result.get("to", "").startswith("/application/o/"):
                logger.debug(" 💡 Flow completed successfully, exchanging for tokens")
                try:
                    token_result = await provider.get_oauth_token(
                        grant_type="password",
                        username=username,
                        password=password,
                    )
                    logger.debug(" ✅ Token exchange successful")
                    return token_result
                except Exception as e:
                    logger.error(f" ❌ Token exchange failed: {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=" ❌ Authentication failed: Token exchange failed",
                    )
            else:
                logger.error(" ❌ Authentication failed: Flow did not complete successfully")
                logger.error(f" ❌ Flow result: {flow_result}")
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
    """
    Execute the Authentik authentication flow through its various stages.

    :param httpx.AsyncClient client: The HTTP client to use
    :param AuthentikProvider provider: The Authentik provider instance
    :param str username: The username to authenticate
    :param str password: The user's password
    :param Optional[str] mfa_code: Optional MFA code
    :return Dict[str, Any]: The final flow result
    :raises HTTPException: If authentication fails
    """
    # Start authentication flow
    flow_result = await _start_authentication_flow(client, provider)
    logger.debug(f" 💡 Initial flow state: {flow_result}")

    # Store flow state
    flow_state = {
        "session": flow_result.get("session", {}).get("uid"),
        "component": flow_result.get("component"),
        "pending_user": flow_result.get("pending_user"),
        "pending_user_avatar": flow_result.get("pending_user_avatar"),
    }
    logger.debug(f" 💡 Flow state: {flow_state}")

    # Handle identification stage
    flow_result = await _handle_identification_stage(client, provider, flow_result, username)
    logger.debug(f" 💡 After identification: {flow_result}")

    # Log user state after identification
    if flow_result.get("pending_user"):
        logger.info(f" 💡 User identified: {flow_result.get('pending_user')}")
        logger.info(f" 💡 User state: {flow_result.get('user_state', 'unknown')}")
        logger.info(f" 💡 Flow type: {flow_result.get('type')}")
        logger.info(f" 💡 Next component: {flow_result.get('component')}")

    # Update flow state
    flow_state.update(
        {
            "session": flow_result.get("session", {}).get("uid") or flow_state["session"],
            "component": flow_result.get("component"),
            "pending_user": flow_result.get("pending_user") or flow_state["pending_user"],
        }
    )

    # Handle password stage if needed
    if flow_result.get("component") == "ak-stage-password":
        flow_result = await _handle_password_stage(client, provider, password, flow_state)
        logger.debug(f" 💡 After password: {flow_result}")

    # Handle MFA if needed
    if flow_result.get("component") == "ak-stage-authenticator-validate":
        flow_result = await _handle_mfa_stage(client, provider, mfa_code)
        logger.debug(f" 💡 After MFA: {flow_result}")

    # Handle any redirects
    if flow_result.get("type") == "redirect" and flow_result.get("to", "").startswith("/if/"):
        flow_result = await _handle_redirect(client, provider, flow_result)
        logger.debug(f" 💡 After redirect: {flow_result}")

    return flow_result


async def _start_authentication_flow(client: httpx.AsyncClient, provider: AuthentikProvider) -> Dict[str, Any]:
    """Start the authentication flow and return initial flow data."""
    result = await provider._make_request("GET", provider.flow_url, client=client)
    logger.debug(f" 💡 Flow response: {result}")
    return result


async def _handle_identification_stage(
    client: httpx.AsyncClient,
    provider: AuthentikProvider,
    flow_data: Dict[str, Any],
    username: str,
) -> Dict[str, Any]:
    """Handle the identification stage of the authentication flow."""
    # Get the component from the flow data
    component = flow_data.get("component", "")
    if not component:
        logger.error(" ❌ No component found in flow data")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=" ❌ Invalid flow state",
        )

    # Include the flow session if available
    payload = {
        "component": component,
        "uid_field": username,
    }
    if flow_data.get("session", {}).get("uid"):
        payload["session"] = flow_data["session"]["uid"]

    result = await provider._make_request(
        "POST",
        provider.flow_url,
        json=payload,
        client=client,
    )
    logger.debug(f" 💡 Identification stage response: {result}")
    return result


async def _handle_password_stage(
    client: httpx.AsyncClient,
    provider: AuthentikProvider,
    password: str,
    flow_state: Dict[str, Any],
) -> Dict[str, Any]:
    """Handle the password stage of the authentication flow."""
    try:
        # Log the request we're about to make
        logger.debug(" 💡 Sending password stage request")
        logger.debug(f" 💡 Using flow state: {flow_state}")

        # Build the payload with flow state
        payload = {
            "component": "ak-stage-password",
            "password": password,
        }
        if flow_state.get("session"):
            payload["session"] = flow_state["session"]
        if flow_state.get("pending_user"):
            payload["pending_user"] = flow_state["pending_user"]

        result = await provider._make_request(
            "POST",
            provider.flow_url,
            json=payload,
            client=client,
        )

        # Log the complete response for debugging
        logger.debug(f" 💡 Complete password stage response: {result}")

        # Check for password validation errors
        if result.get("response_errors", {}).get("password"):
            errors = result["response_errors"]["password"]
            error_msg = errors[0].get("string", "Invalid password") if errors else "Invalid password"
            logger.error(f" ❌ Password validation failed: {error_msg}")
            logger.error(f" ❌ Full error context: {result.get('response_errors')}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f" ❌ {error_msg}",
            )

        # Check if we got a successful response
        if result.get("type") == "redirect" or not result.get("response_errors"):
            logger.debug(" ��� Password stage completed successfully")
            logger.debug(f" 💡 Next step: {result.get('type')} -> {result.get('to')}")
            return result
        else:
            logger.error(f" ❌ Unexpected password stage response type: {result.get('type')}")
            logger.error(f" ❌ Full response context: {result}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=" ❌ Authentication failed: Invalid response from server",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f" ❌ Password stage error: {str(e)}")
        logger.error(" ❌ This is an unexpected error, not a normal auth failure")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f" ❌ Password stage failed: {str(e)}",
        )


async def _handle_mfa_stage(
    client: httpx.AsyncClient, provider: AuthentikProvider, mfa_code: Optional[str]
) -> Dict[str, Any]:
    """Handle the MFA stage of the authentication flow."""
    if not mfa_code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" ❌ MFA code required",
            headers={"X-MFA-Required": "true"},
        )

    result = await provider._make_request(
        "POST",
        provider.flow_url,
        json={"component": "ak-stage-authenticator-validate", "code": mfa_code},
        client=client,
    )
    logger.debug(f" 💡 MFA stage response: {result}")
    return result


async def _handle_redirect(
    client: httpx.AsyncClient, provider: AuthentikProvider, flow_result: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle flow redirects."""
    redirect_url = flow_result.get("to", "")
    logger.debug(f" 💡 Following redirect to: {redirect_url}")

    if not redirect_url.startswith("http"):
        redirect_url = f"{provider.base_url}{redirect_url}"

    result = await provider._make_request("GET", redirect_url, client=client)
    logger.debug(f" 💡 Redirect response: {result}")
    return result
