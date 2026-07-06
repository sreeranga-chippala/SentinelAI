from __future__ import annotations

import asyncio

from mcp_servers.population.tools import (
    compare_population,
    get_population,
)


async def main() -> None:

    print("\nFetching Bengaluru population...\n")

    result = await get_population(
        city="Bengaluru",
    )

    print(result)

    print("\nComparing Bengaluru and Mysuru...\n")

    comparison = await compare_population(
        city1="Bengaluru",
        city2="Mysuru",
    )

    print(comparison)


if __name__ == "__main__":
    asyncio.run(main())