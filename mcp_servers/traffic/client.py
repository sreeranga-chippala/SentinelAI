"""
SentinelAI - Traffic MCP Client

Provides a singleton MCP connection for the Traffic Server.
"""

from __future__ import annotations

import sys

from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)

from mcp import StdioServerParameters


_connection: StdioConnectionParams | None = None


def get_traffic_connection() -> StdioConnectionParams:
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
                    "mcp_servers.traffic.server",
                ],

            ),

            timeout=120,

        )

    return _connection