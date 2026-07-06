"""
SentinelAI - Hospital MCP Client

Provides a singleton MCP connection for the Hospital Server.
"""

from __future__ import annotations

import sys

from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)

from mcp import StdioServerParameters


_connection: StdioConnectionParams | None = None


def get_hospital_connection() -> StdioConnectionParams:
    """
    Returns a singleton MCP connection.
    """

    global _connection

    if _connection is None:

        _connection = StdioConnectionParams(

            server_params=StdioServerParameters(

                command=sys.executable,

                args=[
                    "-m",
                    "mcp_servers.hospital.server",
                ],

            ),

            # keep the connection alive longer

            timeout=120,

        )

    return _connection