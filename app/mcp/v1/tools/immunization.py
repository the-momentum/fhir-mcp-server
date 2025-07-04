from fastmcp import FastMCP

from app.services.medplum.medplum_client import medplum_client
from app.schemas.fhir_schemas import FhirQueryResponse, FhirQueryRequest, FhirError


immunization_router = FastMCP(name="Immunization Request MCP")


@immunization_router.tool
async def request_immunization_resource(
    request: FhirQueryRequest,
) -> FhirQueryResponse | FhirError:
    """
    Makes an HTTP request to the FHIR server.
    Use this tool to perform CRUD operations only on the FHIR Immunization resource.
    Rules:
        - When creating or updating an immunization, use only the data explicitly provided by the user.
        - Do not guess, auto-fill, or assume any missing data.
        - When deleting an immunization, ask the user for confirmation with details of the immunization and wait for the user's confirmation.
        - Provide links to the app (not api) immunization resource in the final response.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        path: Resource path (e.g., "/Immunization", "/Immunization?patient=Patient/123")
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
