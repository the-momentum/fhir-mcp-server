"""
This module contains the tool for making generic requests to the FHIR server, when the other tools are not applicable.
"""

from fastmcp import FastMCP

from app.services.medplum.medplum_client import medplum_client
from app.schemas.fhir_schemas import FhirQueryResponse, FhirQueryRequest, FhirError


generic_router = FastMCP(name="Generic Request MCP")


@generic_router.tool
async def request_generic_resource(
    request: FhirQueryRequest,
) -> FhirQueryResponse | FhirError:
    """
    Makes an HTTP request to the FHIR server.
    Use this tool to perform CRUD operations on any FHIR resource ONLY if the other tools are not applicable.

    Rules:
        - When creating or updating a resource, use only the data explicitly provided by the user.
        - Do not guess, auto-fill, or assume any missing data.
        - When deleting a resource, ask the user for confirmation with details of the resource and wait for the user's confirmation.
        - Provide links to the app (not api) resource in the final response.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        path: Resource path
        body: Optional JSON data for POST/PUT requests)

    Returns:
        JSON response from the FHIR server
    """

    try:
        response = medplum_client.request(
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
