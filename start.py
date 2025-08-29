import argparse
import os
import subprocess
import sys
from pathlib import Path


def get_project_dir() -> Path:
    return Path(__file__).parent.resolve()


def main() -> None:
    default_transport = os.getenv("TRANSPORT_MODE", "stdio")

    parser = argparse.ArgumentParser(description="Start the FastMCP application")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "https"],
        default=default_transport,
        help=f"Transport mode for the MCP server (default: {default_transport})",
    )

    args = parser.parse_args()
    project_dir = get_project_dir()

    print(f"Starting the FastMCP application in {args.transport} mode...", file=sys.stderr)

    if args.transport == "https":
        cmd = [
            "uv",
            "run",
            "--directory",
            str(project_dir),
            "python",
            "-m",
            "app.main",
        ]
    else:
        cmd = [
            "uv",
            "run",
            "--directory",
            str(project_dir),
            "fastmcp",
            "run",
            "app/main.py",
            "--transport",
            args.transport,
        ]

    print(f"Executing: {' '.join(cmd)}", file=sys.stderr)

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
