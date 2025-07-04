from fastmcp import FastMCP

from app.services.medplum.medplum_client import medplum_client
from app.schemas.fhir_schemas import FhirQueryResponse, FhirQueryRequest, FhirError


allergy_intolerance_request_router = FastMCP(name="Allergy Intolerance Request MCP")


@allergy_intolerance_request_router.tool
async def request_allergy_intolerance_resource(
    request: FhirQueryRequest,
) -> FhirQueryResponse | FhirError:
    """
    Makes an HTTP request to the FHIR server.
    Use this tool to perform CRUD operations only on the FHIR AllergyIntolerance resource.
    Rules:
        - When creating or updating an allergy intolerance, use only the data explicitly provided by the user.
        - Do not guess, auto-fill, or assume any missing data.
        - When deleting an allergy intolerance, ask the user for confirmation with details of the allergy intolerance and wait for the user's confirmation.
        - Provide links to the app (not api) allergy intolerance resource in the final response.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        path: Resource path (e.g., "/AllergyIntolerance", "/AllergyIntolerance?patient=Patient/123")
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
