import requests
from fastapi import status

from app.mcp.exceptions import APICustomError


def handle_requests_exceptions(e: Exception, url: str) -> None:
    """
    Handle all possible request exceptions from the Medplum API.

    Args:
        e: The caught exception
        url: The URL that was being accessed when the error occurred

    Raises:
        APICustomError: A standardized API error with appropriate status and message
    """

    if isinstance(e, requests.exceptions.HTTPError):
        response = e.response
        raise APICustomError(
            status=response.status_code if response else status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="medplum_api_error",
            message=f"Medplum API returned HTTP error: {response.text if response else str(e)}",
            ctx={"url": url},
        )
    elif isinstance(e, requests.exceptions.RequestException):
        raise APICustomError(
            status=status.HTTP_502_BAD_GATEWAY,
            code="medplum_connection_error",
            message="Failed to connect to Medplum API.",
        )
    elif isinstance(e, ValueError):
        raise APICustomError(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="medplum_invalid_response",
            message="Medplum API returned invalid JSON.",
        )
    else:
        raise APICustomError(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="unknown_error",
            message="Unexpected error occurred.",
        )
