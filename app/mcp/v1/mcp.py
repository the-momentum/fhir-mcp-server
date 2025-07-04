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
)

mcp_router = FastMCP(name="Main MCP")

mcp_router.mount(patient.patient_request_router)
mcp_router.mount(observation.observation_request_router)
mcp_router.mount(generic.generic_request_router)
mcp_router.mount(encounter.encounter_request_router)
mcp_router.mount(condition.condition_request_router)
mcp_router.mount(allergy_intolerance.allergy_intolerance_request_router)
mcp_router.mount(immunization.immunization_request_router)
mcp_router.mount(family_member_history.family_member_history_request_router)
mcp_router.mount(medication.medication_request_router)
