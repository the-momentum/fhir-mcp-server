import requests
from fastapi import HTTPException, status

from app.config import settings


class OAuthClient:
    """Handles OAuth2 HTTP requests for token exchange."""

    def __init__(self, base_url: str, timeout: int | None = None):
        self.base_url = base_url
        self.timeout = timeout or settings.FHIR_SERVER_TIMEOUT
        self.token_url = f"{self.base_url}/oauth2/token"
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def exchange_client_credentials(
        self,
        client_id: str,
        client_secret: str,
    ) -> dict:
        """Exchange client credentials for access token."""
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }

        response = requests.post(
            self.token_url,
            data=data,
            headers=self.headers,
            timeout=self.timeout,
        )

        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid client credentials",
            )

        return response.json()

    def exchange_authorization_code(
        self,
        client_id: str,
        code: str,
        redirect_uri: str,
    ) -> dict:
        """Exchange authorization code for access token."""
        if not code:
            raise ValueError(
                "Authorization code is required. Call set_authorization_code() first.",
            )
        if not redirect_uri:
            raise ValueError(
                "Redirect URI is required for authorization code flow. Set it in config.",
            )

        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "code": code,
            "redirect_uri": redirect_uri,
        }

        response = requests.post(
            self.token_url,
            data=data,
            headers=self.headers,
            timeout=self.timeout,
        )

        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code",
            )

        return response.json()
