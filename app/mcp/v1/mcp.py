from fastmcp import FastMCP

from app.mcp.v1.tools import (
    patient,
    observation,
    generic,
    encounter,
    condition,
    allergy_intolerance,
    immunization,
    family_member_history,
    medication,
    document_reference,
)

mcp_router = FastMCP(name="Main MCP")

mcp_router.mount(patient.patient_router)
mcp_router.mount(generic.generic_router)
mcp_router.mount(observation.observation_router)
mcp_router.mount(encounter.encounter_router)
mcp_router.mount(condition.condition_router)
mcp_router.mount(allergy_intolerance.allergy_intolerance_router)
mcp_router.mount(immunization.immunization_router)
mcp_router.mount(family_member_history.family_member_history_router)
mcp_router.mount(medication.medication_router)
mcp_router.mount(document_reference.document_reference_router)
