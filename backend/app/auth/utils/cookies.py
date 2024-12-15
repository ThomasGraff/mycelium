"""Cookie management utilities."""

from typing import Dict

from fastapi import Response


def set_auth_cookies(response: Response, auth_result: Dict[str, str]) -> None:
    """
    Set authentication cookies in the response.

    :param Response response: FastAPI response object
    :param Dict[str, str] auth_result: Authentication result containing tokens
    """
    # Set access token cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {auth_result['access_token']}",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,  # 1 hour, matching Authentik's default
        path="/",
    )

    # Set refresh token cookie if available
    if auth_result.get("refresh_token"):
        response.set_cookie(
            key="refresh_token",
            value=auth_result["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 30,  # 30 days
            path="/",
        )


def clear_auth_cookies(response: Response) -> None:
    """
    Clear authentication cookies from the response.

    :param Response response: FastAPI response object
    """
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
