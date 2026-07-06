import asyncio

from mcp_servers.communication.tools import (
    generate_emergency_message,
)


async def main():
    result = await generate_emergency_message(
        incident_type="Flood",
        location="Bengaluru",
        severity="High",
        instructions="Evacuate immediately to higher ground.",
    )

    print(result)


asyncio.run(main())