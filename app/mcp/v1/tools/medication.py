from typing import Any, Literal

from fastmcp import FastMCP

from app.schemas.fhir_schemas import FhirError, FhirQueryRequest, FhirQueryResponse
from app.services.fhir.fhir_client import fhir_client

medication_router = FastMCP(name="Medication Request MCP")


@medication_router.tool
async def request_medication_resource(
    method: Literal["GET", "POST", "PUT", "DELETE"],
    path: str,
    body: dict[str, Any] | None = None,
) -> FhirQueryResponse | FhirError:
    """
    Makes an HTTP request to the FHIR server.
    Use this tool to perform CRUD operations only on the FHIR Medication resource.
    Rules:
        - When creating or updating a medication, use only the data explicitly provided by
          the user.
        - Do not guess, auto-fill, or assume any missing data.
        - When deleting a medication, ask the user for confirmation with details of the
          medication and wait for the user's confirmation.
        - Provide links to the app (not api) medication resource in the final response.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        path: Resource path (e.g., "/Medication", "/Medication?code=12345")
        body: Optional JSON data for POST/PUT requests)

    Returns:
        JSON response from the FHIR server
    """

    request = FhirQueryRequest(method=method, path=path, body=body)

    try:
        response = fhir_client.request(
            method=request.method,
            path=request.path,
            json=request.body,
        )
    except Exception as e:
        return FhirError(
            error_message=str(e),
            method=request.method,
            path=request.path,
            body=request.body,
        )

    return response
