"""
Priority MCP Server
-------------------
Exposes priority calculation tools via FastMCP.
"""

import logging

from mcp.server.fastmcp import FastMCP

from mcp_servers.priority.tools import calculate_priority

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

mcp = FastMCP("Priority MCP Server")


@mcp.tool()
async def calculate_incident_priority(
    severity: int,
    affected_people: int,
    critical_injuries: int,
    distance_km: float,
    weather: str,
    road_access: str,
):
    """
    Calculate disaster response priority.

    Parameters
    ----------
    severity : int (1-10)

    affected_people : int

    critical_injuries : int

    distance_km : float

    weather : clear/clouds/rain/thunderstorm/etc.

    road_access : good/moderate/difficult/blocked
    """

    logger.info(
        "Calculating priority for incident (severity=%s)",
        severity,
    )

    return await calculate_priority(
        severity=severity,
        affected_people=affected_people,
        critical_injuries=critical_injuries,
        distance_km=distance_km,
        weather=weather,
        road_access=road_access,
    )


if __name__ == "__main__":
    logger.info("Starting Priority MCP Server...")
    mcp.run()