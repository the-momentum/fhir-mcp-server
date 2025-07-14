from fastmcp import FastMCP

from app.services.fhir.fhir_client import fhir_client
from app.schemas.fhir_schemas import FhirQueryResponse, FhirQueryRequest, FhirError


patient_router = FastMCP(name="Patient Request MCP")


@patient_router.tool
async def request_patient_resource(
    request: FhirQueryRequest,
) -> FhirQueryResponse | FhirError:
    """
    Makes an HTTP request to the FHIR server.
    Use this tool to perform CRUD operations only on the FHIR Patient resource.
    Rules:
        - When creating or updating a patient, use only the data explicitly provided by the user.
        - Do not guess, auto-fill, or assume any missing data.
        - When deleting a patient, ask the user for confirmation with details of the patient and wait for the user's confirmation.
        - Provide links to the app (not api) patient resource in the final response.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        path: Resource path (e.g., "/Patient", "/Patient?name=John%20Doe")
        body: Optional JSON data for POST/PUT requests)

    Returns:
        JSON response from the FHIR server
    """

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
