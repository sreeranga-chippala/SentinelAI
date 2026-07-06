import asyncio

from dotenv import load_dotenv

load_dotenv()

from mcp_servers.traffic.tools import get_route_information


async def main():

    result = await get_route_information(
    origin="Bengaluru",
    destination="Mysuru",
)

    print(result)


asyncio.run(main())