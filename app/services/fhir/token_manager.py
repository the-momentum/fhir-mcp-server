from datetime import datetime, timedelta, timezone

import requests
from fastapi import HTTPException, status

from app.config import settings


class Token:
    def __init__(self, access_token: str | None = None, expires_at: datetime | None = None):
        """
        Args:
            access_token (str): The access token
            expires_at (datetime): The expiration timestamp
        """

        self.access_token = access_token
        self.expires_at = expires_at


class AccessTokenManager:
    """Manages access token lifecycle for client credentials flow.

    This class handles the automatic fetching and renewal of access tokens
    using the client credentials grant type.

    Args:
        client_id (str)
        client_secret (str)
        base_url (str): The base URL of the FHIR server
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str,
        token: Token | None = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.token = token if token else Token()

    def _fetch_token(self) -> None:
        auth_url = f"{self.base_url}/oauth2/token"
        client_credentials = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(
            auth_url,
            data=client_credentials,
            timeout=settings.FHIR_SERVER_TIMEOUT,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid client credentials",
            )
        token_data = response.json()
        self.token.access_token = token_data["access_token"]

        expires_in = token_data.get("expires_in", 3600)
        expires_in = max(expires_in - 60, 30)  # minimum 30 seconds buffer
        self.token.expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

    def _is_expired(self) -> bool:
        if self.token.expires_at is None:
            return True
        return datetime.now(timezone.utc) >= self.token.expires_at

    def get_token(self) -> str:
        if self.token.access_token is None or self._is_expired():
            self._fetch_token()
        assert self.token.access_token is not None
        return self.token.access_token
