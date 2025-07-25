from fastapi import status
from requests.exceptions import HTTPError, RequestException

from app.mcp.exceptions import APICustomError


def handle_requests_exceptions(e: Exception, url: str) -> None:
    """
    Handle all possible request exceptions from the FHIR API.

    Args:
        e: The caught exception
        url: The URL that was being accessed when the error occurred

    Raises:
        APICustomError: A standardized API error with appropriate status and message
    """

    if isinstance(e, HTTPError):
        response = e.response
        raise APICustomError(
            status=response.status_code if response else status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="fhir_api_error",
            message=f"FHIR API returned HTTP error: {response.text if response else str(e)}",
            ctx={"url": url},
        )
    if isinstance(e, RequestException):
        raise APICustomError(
            status=status.HTTP_502_BAD_GATEWAY,
            code="fhir_connection_error",
            message="Failed to connect to FHIR API.",
        )
    if isinstance(e, ValueError):
        raise APICustomError(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="fhir_invalid_response",
            message="FHIR API returned invalid JSON.",
        )
    raise APICustomError(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="unknown_error",
        message="Unexpected error occurred.",
    )
