from datetime import datetime
from enum import Enum


class AuthMethod(Enum):
    CLIENT_CREDENTIALS = "client_credentials"
    AUTHORIZATION_CODE = "authorization_code"


class Token:
    def __init__(self, access_token: str | None = None, expires_at: datetime | None = None):
        """
        Args:
            access_token (str): The access token
            expires_at (datetime): The expiration timestamp
        """
        self.access_token = access_token
        self.expires_at = expires_at
