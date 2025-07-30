import requests
from requests.exceptions import RequestException

from app.config import settings
from app.schemas.fhir_schemas import FhirMethod, FhirQueryResponse
from app.services.fhir.errors import handle_requests_exceptions
from app.services.fhir.models import AuthMethod
from app.services.fhir.token_manager import AccessTokenManager
from app.utils.auth import BearerAuth


class FhirClient:
    """
    A client for interacting with the FHIR API.

    This class provides a wrapper around the FHIR API, handling authentication
    and request management. It uses the AccessTokenManager to maintain valid tokens
    for API requests.

    Attributes:
        base_url (str): The base URL of the FHIR API server
        token_manager (AccessTokenManager): Manages token lifecycle
    """

    def __init__(self):
        """Initialize the FHIR server client with settings configuration."""
        self.base_url = settings.FHIR_SERVER_HOST + settings.FHIR_BASE_URL

        # Determine authentication method from settings
        auth_method = AuthMethod(settings.OAUTH2_AUTH_METHOD)

        # Initialize token manager based on authentication method
        if auth_method == AuthMethod.CLIENT_CREDENTIALS:
            self.token_manager = AccessTokenManager(
                settings.FHIR_SERVER_CLIENT_ID,
                settings.FHIR_SERVER_CLIENT_SECRET,
                settings.FHIR_SERVER_HOST,
                auth_method=auth_method,
            )
        elif auth_method == AuthMethod.AUTHORIZATION_CODE:
            self.token_manager = AccessTokenManager(
                settings.FHIR_SERVER_CLIENT_ID,
                settings.FHIR_SERVER_CLIENT_SECRET,
                settings.FHIR_SERVER_HOST,
                auth_method=auth_method,
                redirect_uri=settings.OAUTH2_REDIRECT_URI,
            )
        else:
            raise ValueError(f"Unsupported authentication method: {auth_method}")

    def request(self, method: FhirMethod, path: str, **kwargs) -> FhirQueryResponse:
        """
        Performs a token-authenticated HTTP request to the FHIR API.

        Automatically adds the `Authorization: Bearer <token>` header to the request.

        Args:
            method (str): HTTP method.
            path (str): API endpoint path.
            **kwargs: Extra arguments for `requests.request`.

        Returns:
            Any: JSON-decoded response.
        """

        auth = BearerAuth(self.token_manager.get_token())
        url = f"{self.base_url}{path}"

        try:
            response = requests.request(
                method,
                url,
                auth=auth,
                timeout=settings.FHIR_SERVER_TIMEOUT,
                **kwargs,
            )
            response.raise_for_status()
            return FhirQueryResponse(
                method=method,
                path=url,
                body=kwargs.get("json", {}),
                response=response.json(),
            )
        except (RequestException, ValueError) as e:
            handle_requests_exceptions(e, url)
            raise e

    def get_authorization_url(self, state: str | None = None) -> str:
        """Get the authorization URL for authorization code flow.

        Args:
            state (str, optional): A random string to prevent CSRF attacks

        Returns:
            str: The authorization URL
        """
        return self.token_manager.get_authorization_url(state)

    def set_authorization_code(self, code: str) -> None:
        """Set the authorization code for token exchange.

        Args:
            code (str): The authorization code received from the OAuth2 server
        """
        self.token_manager.set_authorization_code(code)

    def is_authorization_code_flow(self) -> bool:
        """Check if the client is configured for authorization code flow.

        Returns:
            bool: True if using authorization code flow
        """
        return self.token_manager.auth_method == AuthMethod.AUTHORIZATION_CODE


fhir_client = FhirClient()
