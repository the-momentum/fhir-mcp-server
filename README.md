# Team Python - FastAPI base Boilerplate

1. Install uv.
2. `uv sync --group lint` (install app dependencies and lint group)
3. `uv run pre-commit run --all-files`

## Config files

### Docker
```
{
    "mcpServers": {
        "docker-mcp-server": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "--init",
                "-v", # optional - volume for reload
                "<project-path>/app:/root_project/app", # optional - volume for reload
                "mcp-server:latest"
            ]
        }
    }
}
```
