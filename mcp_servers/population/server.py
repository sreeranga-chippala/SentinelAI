"""
SentinelAI - Population MCP Server

Exposes Population tools using the official MCP FastMCP server.
"""

from __future__ import annotations

import logging

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from mcp_servers.population.tools import (
    compare_population,
    get_population,
    health_check,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

mcp = FastMCP("SentinelAI Population Server")


@mcp.tool()
async def population(
    city: str,
) -> dict:
    """
    Retrieve population information for a city.
    """

    return await get_population(city)


@mcp.tool()
async def compare(
    city1: str,
    city2: str,
) -> dict:
    """
    Compare population of two cities.
    """

    return await compare_population(
        city1,
        city2,
    )


@mcp.tool()
async def ping() -> dict:
    """
    Health check.
    """

    return await health_check()


if __name__ == "__main__":
    logger.info("Starting Population MCP Server...")
    mcp.run()