from typing import Any, Literal

from pydantic import BaseModel, Field

type FhirMethod = Literal["GET", "POST", "PUT", "DELETE"]


class FhirQueryRequest(BaseModel):
    """Request to the FHIR resource."""

    method: FhirMethod = Field(
        ..., description="The HTTP method used to query the FHIR resource"
    )
    path: str = Field(..., description="The path of the FHIR resource")
    body: dict[str, Any] | None = Field(
        None,
        description="The body of the FHIR resource. "
        "If the method is GET, the body is not required.",
    )


class FhirQueryResponse(FhirQueryRequest):
    """Response from the FHIR resource with extra fields from the request."""

    response: Any = Field(..., description="The response from the FHIR resource")


class FhirQueryResponseList(BaseModel):
    responses: list[FhirQueryResponse] = Field(
        ..., description="The list of FHIR resource responses"
    )