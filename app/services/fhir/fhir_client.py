import requests
from requests.exceptions import RequestException

from app.config import settings
from app.schemas.fhir_schemas import FhirMethod, FhirQueryResponse
from app.services.fhir.errors import handle_requests_exceptions
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
        self.token_manager = AccessTokenManager(
            settings.FHIR_SERVER_CLIENT_ID,
            settings.FHIR_SERVER_CLIENT_SECRET,
            settings.FHIR_SERVER_HOST,
        )

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


fhir_client = FhirClient()
