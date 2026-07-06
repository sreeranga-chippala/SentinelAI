"""
Communication MCP Client
"""

import sys

from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)
from mcp import StdioServerParameters


def get_communication_connection() -> McpToolset:
    """
    Returns an MCP Toolset connected to the Communication MCP server.
    """

    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command=sys.executable,
                args=[
                    "-m",
                    "mcp_servers.communication.server",
                ],
            )
        )
    )