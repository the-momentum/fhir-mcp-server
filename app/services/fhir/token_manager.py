from abc import ABC

from app.config import settings
from app.services.fhir.models import AuthMethod, Token
from app.services.fhir.oauth_client import OAuthClient
from app.utils.token_utils import (
    build_authorization_url,
    calculate_token_expiry,
    is_token_expired,
    should_refresh_token,
    validate_token_response,
)


class TokenLifecycleMixin(ABC):
    """Mixin for token lifecycle management."""

    def _process_token_response(self, token_data: dict) -> None:
        validate_token_response(token_data)

        self.token.access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 3600)
        self.token.expires_at = calculate_token_expiry(expires_in)

    def _is_expired(self) -> bool:
        return is_token_expired(self.token.expires_at)

    def _should_refresh_token(self) -> bool:
        return should_refresh_token(self.token.expires_at)

    def get_token(self) -> str:
        if self.token.access_token is None or self._should_refresh_token():
            self._fetch_token()
        assert self.token.access_token is not None
        return self.token.access_token


class TokenFetcherMixin(ABC):
    """Mixin for token fetching logic."""

    def _fetch_token(self) -> None:
        if self.auth_method == AuthMethod.CLIENT_CREDENTIALS:
            self._fetch_client_credentials_token()
        elif self.auth_method == AuthMethod.AUTHORIZATION_CODE:
            self._fetch_authorization_code_token()
        else:
            raise ValueError(f"Unsupported authentication method: {self.auth_method}")

    def _fetch_client_credentials_token(self) -> None:
        token_data = self.oauth_client.exchange_client_credentials(
            self.client_id,
            self.client_secret,
        )
        self._process_token_response(token_data)

    def _fetch_authorization_code_token(self) -> None:
        token_data = self.oauth_client.exchange_authorization_code(
            self.client_id,
            self.authorization_code,
            self.redirect_uri,
        )
        self._process_token_response(token_data)


class AuthorizationCodeMixin(ABC):
    """Mixin for authorization code flow methods."""

    def get_authorization_url(self, state: str) -> str:
        if self.auth_method != AuthMethod.AUTHORIZATION_CODE:
            raise ValueError("Authorization URL is only available for authorization code flow")

        return build_authorization_url(
            self.base_url,
            self.client_id,
            self.redirect_uri,
            settings.OAUTH2_SCOPE,
            state,
        )

    def set_authorization_code(self, code: str) -> None:
        """Set the authorization code for token exchange."""
        self.authorization_code = code


class AccessTokenManager(TokenLifecycleMixin, TokenFetcherMixin, AuthorizationCodeMixin):
    """Manages access token lifecycle for OAuth2 flows.

    This class handles the automatic fetching and renewal of access tokens
    using either client credentials or authorization code grant types.

    Args:
        client_id (str)
        client_secret (str)
        base_url (str): The base URL of the FHIR server
        auth_method (AuthMethod): The authentication method to use
        redirect_uri (str, optional): Required for authorization code flow
        authorization_code (str, optional): Required for authorization code flow
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str,
        auth_method: AuthMethod = AuthMethod.CLIENT_CREDENTIALS,
        redirect_uri: str | None = None,
        authorization_code: str | None = None,
        token: Token | None = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.auth_method = auth_method
        self.redirect_uri = redirect_uri
        self.authorization_code = authorization_code
        self.token = token if token else Token()
        self.oauth_client = OAuthClient(base_url)
