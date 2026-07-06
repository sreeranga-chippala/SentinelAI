"""
SentinelAI - Weather MCP Server

Exposes Weather tools using the official MCP FastMCP server.
"""

from __future__ import annotations

import logging

from dotenv import load_dotenv

load_dotenv()
import os

print("OPENWEATHER_API_KEY =", bool(os.getenv("OPENWEATHER_API_KEY")))

from mcp.server.fastmcp import FastMCP

from mcp_servers.weather.tools import (
    get_current_weather,
    health_check,
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

mcp = FastMCP("SentinelAI Weather Server")


@mcp.tool()
async def weather(
    city: str,
    country: str = "",
    units: str = "metric",
) -> dict:
    """
    Retrieve the current weather.

    Args:
        city: City name.
        country: Optional ISO country code (e.g. IN, US).
        units: metric | imperial | standard.
    """

    return await get_current_weather(
        city=city,
        country=country if country else None,
        units=units,
    )
@mcp.tool()
async def ping() -> dict:
    """
    Health check tool.
    """

    return await health_check()


if __name__ == "__main__":
    logger.info("Starting Weather MCP Server...")
    mcp.run()