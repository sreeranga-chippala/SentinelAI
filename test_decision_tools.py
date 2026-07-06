import asyncio

from mcp_servers.decision.tools import generate_decision


async def main():

    result = await generate_decision(
        weather="""
Heavy rainfall.
Temperature: 22°C.
Wind Speed: 18 km/h.
""",
        traffic="""
Road congestion on NH-275.
Estimated travel time increased by 25 minutes.
""",
        hospitals="""
3 hospitals available.
57 ICU beds.
112 General beds.
""",
        population="""
Population Density: High.
Estimated affected people: 15,000.
""",
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())