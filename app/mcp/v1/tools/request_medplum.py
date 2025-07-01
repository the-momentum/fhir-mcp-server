from fastmcp import FastMCP

from app.services.medplum.medplum_client import medplum_client
from app.schemas.fhir_schemas import FhirQueryResponse

medplum_request_router = FastMCP(name="Medplum Request MCP")


@medplum_request_router.tool
def create_patient() -> FhirQueryResponse:
    """Create new patient"""
    return medplum_client.request(
        "POST",
        "/Patient",
        json={
            "resourceType": "Patient",
            "name": [{"use": "official", "family": "Smith", "given": ["John"]}],
            "gender": "male",
            "birthDate": "1980-01-01",
        },
    )
