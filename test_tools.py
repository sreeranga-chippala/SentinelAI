import asyncio

from dotenv import load_dotenv

load_dotenv()

from mcp_servers.weather.tools import get_current_weather


async def main():
    result = await get_current_weather(
        latitude=12.9716,
        longitude=77.5946,
    )

    print(result)


asyncio.run(main())