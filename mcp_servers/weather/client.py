"""
SentinelAI - Weather MCP Client

Provides MCP connection parameters for the Google ADK
Weather Agent.
"""

from __future__ import annotations

import sys
from pathlib import Path

from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)

from mcp import StdioServerParameters


def get_weather_connection() -> StdioConnectionParams:
    """
    Returns the stdio connection parameters required
    by MCPToolset.
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
            args=[str(server_file)],
        ),
        timeout=30,
    )