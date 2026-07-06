"""
SentinelAI - Allocation MCP Server

Exposes Allocation tools using FastMCP.
"""

from __future__ import annotations

import logging

from mcp.server.fastmcp import FastMCP

from mcp_servers.allocation.tools import (
    calculate_priority,
    allocate_resources,
    generate_recommendations,
    perform_allocation,
    health_check,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

mcp = FastMCP("SentinelAI Allocation Server")


@mcp.tool()
async def allocation(
    disaster_type: str,
    severity: str,
    affected_people: int,
    available_resources: dict,
) -> dict:
    """
    Complete disaster resource allocation.
    """

    return perform_allocation(
        disaster_type=disaster_type,
        severity=severity,
        affected_people=affected_people,
        available_resources=available_resources,
    )


@mcp.tool()
async def priority(
    disaster_type: str,
    severity: str,
    affected_people: int,
) -> dict:
    """
    Calculate disaster priority.
    """

    return calculate_priority(
        disaster_type,
        severity,
        affected_people,
    )


@mcp.tool()
async def recommend(
    priority: str,
    remaining: dict,
) -> list:
    """
    Generate allocation recommendations.
    """

    return generate_recommendations(
        priority,
        remaining,
    )


@mcp.tool()
async def ping() -> dict:
    """
    Health check.
    """

    return health_check()


if __name__ == "__main__":
    logger.info("Starting Allocation MCP Server...")
    mcp.run()