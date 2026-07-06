"""
SentinelAI - Decision MCP Client
"""

from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)

from mcp import StdioServerParameters


def get_decision_connection() -> StdioConnectionParams:
    """
    Returns the stdio connection for the Decision MCP server.
    """

    return StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[
                "-m",
                "mcp_servers.decision.server",
            ],
        )
    )