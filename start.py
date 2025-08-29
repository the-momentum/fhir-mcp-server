import argparse
import subprocess
import sys
from pathlib import Path


def get_project_dir() -> Path:
    return Path(__file__).parent.resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description="Start the FastMCP application")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "https"],
        default="stdio",
        help="Transport mode for the MCP server (default: stdio)",
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
        ]

        if args.transport == "http":
            cmd.append("--transport")
            cmd.append("http")

    print(f"Executing: {' '.join(cmd)}", file=sys.stderr)

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
