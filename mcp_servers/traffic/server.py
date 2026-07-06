"""
SentinelAI - Traffic MCP Server

Exposes Traffic tools using the official MCP FastMCP server.
"""

from __future__ import annotations

import logging

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from mcp_servers.traffic.tools import (
    get_route_information,
    health_check,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

mcp = FastMCP("SentinelAI Traffic Server")


@mcp.tool()
async def route(
    origin: str,
    destination: str,
) -> dict:
    """
    Compute a traffic-aware driving route.

    Args:
        origin:
            Origin city or address.

        destination:
            Destination city or address.
    """

    return await get_route_information(
        origin=origin,
        destination=destination,
    )


@mcp.tool()
async def ping() -> dict:
    """
    Health check tool.
    """

    return await health_check()


if __name__ == "__main__":
    logger.info("Starting Traffic MCP Server...")
    mcp.run()