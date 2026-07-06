"""
SentinelAI - Hospital MCP Client
"""

from __future__ import annotations

import sys
from pathlib import Path

from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)

from mcp import StdioServerParameters


def get_hospital_connection() -> StdioConnectionParams:
    """
    MCP connection parameters for Hospital Server.
    """

    server_file = (
        Path(__file__)
        .resolve()
        .parent
        / "server.py"
    )

    return StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[
                "-m",
                "mcp_servers.hospital.server",
            ],
        ),
        timeout=30,
    )