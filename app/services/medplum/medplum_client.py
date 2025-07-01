import requests

from app.config import settings
from app.schemas.fhir_schemas import FhirQueryResponse, FhirMethod
from app.services.medplum.errors import handle_requests_exceptions
from app.services.medplum.token_manager import AccessTokenManager
from app.utils.auth import BearerAuth

class MedplumClient:
    """
    A client for interacting with the Medplum FHIR API.

    This class provides a wrapper around the Medplum API, handling authentication
    and request management. It uses the AccessTokenManager to maintain valid tokens
    for API requests.

    Attributes:
        base_url (str): The base URL of the Medplum API server
        token_manager (AccessTokenManager): Manages token lifecycle
    """

    def __init__(self):
        """Initialize the Medplum client with settings configuration."""
        self.base_url = settings.MEDPLUM_HOST + settings.FHIR_BASE_URL
        self.token_manager = AccessTokenManager(
            settings.MEDPLUM_CLIENT_ID,
            settings.MEDPLUM_CLIENT_SECRET.get_secret_value(),
            settings.MEDPLUM_HOST,
        )

    def request(self, method: FhirMethod, path: str, **kwargs) -> FhirQueryResponse:
        """
        Performs a token-authenticated HTTP request to the Medplum API.

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
                method, url, auth=auth, timeout=settings.MEDPLUM_TIMEOUT, **kwargs
            )
            response.raise_for_status()
            return FhirQueryResponse(
                method=method,
                path=url,
                body=kwargs.get("json", {}),
                response=response.json(),
            )
        except (requests.exceptions.RequestException, ValueError) as e:
            handle_requests_exceptions(e, url)
            raise e


medplum_client = MedplumClient()