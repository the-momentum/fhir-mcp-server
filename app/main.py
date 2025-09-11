import sys

import uvicorn
from fastmcp import FastMCP

from app.config import settings
from app.mcp.v1.mcp import mcp_router

print("SETUP -> Setting up the app", file=sys.stderr)

mcp = FastMCP(settings.PROJECT_NAME)

mcp.mount(mcp_router)

# run: uv run fastmcp run app/main.py --transport http
if __name__ == "__main__":
    # uv run python -m app.main
    if settings.TRANSPORT_MODE in ["stdio", "http"]:
        mcp.run(transport="streamable-http")

    elif settings.TRANSPORT_MODE == "https":
        uvicorn.run(
            mcp.http_app,
            host=settings.MCP_SERVER_HOST,
            port=settings.MCP_SERVER_PORT,
            ssl_keyfile=settings.MCP_SERVER_SSL_KEYFILE,
            ssl_certfile=settings.MCP_SERVER_SSL_CERTFILE,
        )
