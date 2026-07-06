import asyncio

from mcp_servers.hospital.tools import find_nearby_hospitals


async def main():
    result = await find_nearby_hospitals("Bengaluru")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())