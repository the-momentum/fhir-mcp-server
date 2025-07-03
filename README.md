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
                "--mount",
                "type=bind,source=<project-path>/config/.env,target=/root_project/.env",
                "--mount", # optional - volume for reload
                "type=bind,source=<project-path>/app,target=/root_project/app", # optional
                "mcp-server:latest"
            ]
        }
    }
}
```
