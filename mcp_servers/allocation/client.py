"""
SentinelAI - Allocation MCP Client

Provides MCP connection parameters for the Google ADK
Allocation Agent.
"""

from __future__ import annotations

import sys

from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)

from mcp import StdioServerParameters


def get_allocation_connection() -> StdioConnectionParams:
    """
    Returns the stdio connection parameters required
    by MCPToolset.
    """

    return StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[
                "-m",
                "mcp_servers.allocation.server",
            ],
        ),
        timeout=30,
    )