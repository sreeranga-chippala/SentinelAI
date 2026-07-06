import asyncio

from mcp_servers.priority.tools import calculate_priority


async def main():

    result = await calculate_priority(
        severity=9,
        affected_people=750,
        critical_injuries=35,
        distance_km=8,
        weather="Heavy Rain",
        road_access="Difficult",
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())