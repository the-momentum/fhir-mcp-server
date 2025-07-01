from fastmcp import FastMCP

from app.mcp.v1.tools import request_medplum

mcp_router = FastMCP(name="Main MCP")

mcp_router.mount(request_medplum.medplum_request_router)
