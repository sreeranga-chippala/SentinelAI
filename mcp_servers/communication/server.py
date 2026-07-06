"""
SentinelAI Communication MCP Server
"""

from mcp.server.fastmcp import FastMCP

from mcp_servers.communication.tools import (
    generate_emergency_message,
    broadcast_status,
    health_check,
)

mcp = FastMCP("Communication MCP")


@mcp.tool()
async def create_emergency_message(
    incident_type: str,
    location: str,
    severity: str,
    instructions: str,
):
    """
    Generate an emergency communication message.
    """
    return await generate_emergency_message(
        incident_type,
        location,
        severity,
        instructions,
    )


@mcp.tool()
async def broadcast_message(
    channel: str,
    message: str,
):
    """
    Broadcast an emergency message.
    """
    return await broadcast_status(
        channel,
        message,
    )


@mcp.tool()
async def communication_health():
    """
    Communication MCP health check.
    """
    return await health_check()


if __name__ == "__main__":
    print("Starting Communication MCP Server...")
    mcp.run()