"""OAuth2 token utilities and helpers."""

from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode


def build_authorization_url(
    base_url: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
) -> str:
    """Build OAuth2 authorization URL with proper encoding.

    Args:
        base_url: OAuth2 server base URL
        client_id: OAuth2 client ID
        redirect_uri: Redirect URI for callback
        scope: OAuth2 scope
        state: CSRF protection state parameter

    Returns:
        Complete authorization URL
    """
    if not state:
        raise ValueError("State parameter is required for security")

    auth_url = f"{base_url}/oauth2/authorize"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "state": state,
    }

    query_string = urlencode(params)
    return f"{auth_url}?{query_string}"


def validate_token_response(token_data: dict) -> None:
    """Validate token response structure.

    Args:
        token_data: Token response from OAuth2 server

    Raises:
        ValueError: If required fields are missing
    """
    required_fields = ["access_token"]
    for field in required_fields:
        if field not in token_data:
            raise ValueError(f"Missing required field in token response: {field}")


def calculate_token_expiry(expires_in: int, buffer_minutes: int = 5) -> datetime:
    """Calculate token expiry with buffer.

    Args:
        expires_in: Token expiry time in seconds
        buffer_minutes: Buffer time before expiry (default: 5 minutes)

    Returns:
        Calculated expiry datetime
    """
    buffer_seconds = max(buffer_minutes * 60, 30)  # minimum 30 seconds
    expires_in = max(expires_in - buffer_seconds, 30)
    return datetime.now(timezone.utc) + timedelta(seconds=expires_in)


def should_refresh_token(expires_at: datetime | None, buffer_minutes: int = 5) -> bool:
    """Check if token should be refreshed.

    Args:
        expires_at: Token expiry datetime
        buffer_minutes: Buffer time before expiry

    Returns:
        True if token should be refreshed
    """
    if not expires_at:
        return True
    buffer_time = timedelta(minutes=buffer_minutes)
    return datetime.now(timezone.utc) >= (expires_at - buffer_time)


def is_token_expired(expires_at: datetime | None) -> bool:
    """Check if token is expired.

    Args:
        expires_at: Token expiry datetime

    Returns:
        True if token is expired
    """
    if not expires_at:
        return True
    return datetime.now(timezone.utc) >= expires_at
