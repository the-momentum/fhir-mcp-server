import sys
from fastmcp import FastMCP

from app.mcp.v1.mcp import mcp_router


print("SETUP -> Setting up the app", file=sys.stderr)
mcp = FastMCP("Demo MCP")

mcp.mount(mcp_router)

if __name__ == "__main__":
    mcp.run()
