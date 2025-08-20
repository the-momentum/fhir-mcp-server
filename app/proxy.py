"""
Proxy server for Claude Desktop to run HTTP MCP server.
"""

from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient

proxy = FastMCP.as_proxy(
    ProxyClient("http://localhost:8000/mcp/"),
    name="MyProxy",
)

if __name__ == "__main__":
    proxy.run()
