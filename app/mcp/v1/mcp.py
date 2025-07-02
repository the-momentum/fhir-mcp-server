from fastmcp import FastMCP

from app.mcp.v1.tools import patient

mcp_router = FastMCP(name="Main MCP")

mcp_router.mount(patient.patient_request_router)
