"""
SentinelAI - Decision MCP Server
"""

from __future__ import annotations

import logging

from mcp.server.fastmcp import FastMCP

from mcp_servers.decision.tools import (
    generate_decision,
    health_check,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

mcp = FastMCP("SentinelAI Decision Server")


@mcp.tool()
async def decision(
    weather: str,
    traffic: str,
    hospitals: str,
    population: str,
) -> dict:
    """
    Generate an emergency decision.
    """

    return await generate_decision(
        weather=weather,
        traffic=traffic,
        hospitals=hospitals,
        population=population,
    )


@mcp.tool()
async def ping() -> dict:
    """
    Health check.
    """

    return await health_check()


if __name__ == "__main__":
    logger.info("Starting Decision MCP Server...")
    mcp.run()