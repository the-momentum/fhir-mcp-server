"""
Test client to check out how MCP server tools reacts.
"""

import asyncio

from fastmcp import Client

# from fastmcp.client.transports import StdioTransport
from app.schemas.fhir_schemas import FhirQueryRequest

# http
client = Client("http://127.0.0.1:8000/mcp")

# stdio
# client = Client(StdioTransport(
#     command=".venv/bin//python",
#     args=["-m", "app.main"]
# ))

request = FhirQueryRequest(
    method="GET",
    path="/Patient",
    body={
        "name": [
            {
                "use": "official",
                "given": [
                    "Lionel",
                ],
                "family": "Messi",
            },
        ],
    },
)


async def main() -> None:
    # uv run python -m  app.client
    async with client:
        await client.ping()
        # tools = await client.list_tools()
        # resources = await client.list_resources()
        # prompts = await client.list_prompts()
        result = await client.call_tool("request_patient_resource", {"request": request})
        print(result)


asyncio.run(main())
