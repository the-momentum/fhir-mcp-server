#!/bin/bash
set -e

# Init app
# Redirect to stderr with >&2 (for mcp usage)
echo "Starting the FastMCP application..." >&2
if [ "$DEBUG" = "True" ]; then
    # Todo: enable hot reload with uvicorn
    echo "DEBUG mode is enabled" >&2
    uv run fastmcp run app/main.py
else
    uv run fastmcp run app/main.py
fi
