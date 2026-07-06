"""
SentinelAI - Population MCP Tools

Uses the OpenDataSoft Geonames dataset
to retrieve city population information.

No API key required.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

BASE_URL = (
    "https://public.opendatasoft.com/api/explore/v2.1/"
    "catalog/datasets/geonames-all-cities-with-a-population-1000/records"
)


class PopulationToolException(Exception):
    """Population tool exception."""


async def get_population(
    city: str,
) -> dict[str, Any]:
    """
    Retrieve population information for a city.
    """

    params = {
        "where": f"name='{city}'",
        "limit": 1,
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                BASE_URL,
                params=params,
            )

        response.raise_for_status()

        payload = response.json()

    except httpx.HTTPStatusError as exc:
        logger.exception("Population API HTTP error.")

        raise PopulationToolException(
            f"HTTP {exc.response.status_code}"
        ) from exc

    except httpx.RequestError as exc:
        logger.exception("Population API connection error.")

        raise PopulationToolException(
            "Unable to contact Population API."
        ) from exc

    results = payload.get("results", [])

    if not results:
        raise PopulationToolException(
            f"No population information found for '{city}'."
        )

    result = results[0]

    coordinates = result.get("coordinates", {})

    return {
        "success": True,
        "city": result.get("name"),
        "country": result.get("cou_name_en"),
        "population": result.get("population"),
        "latitude": coordinates.get("lat"),
        "longitude": coordinates.get("lon"),
        "timezone": result.get("timezone"),
    }


async def compare_population(
    city1: str,
    city2: str,
) -> dict[str, Any]:
    """
    Compare population between two cities.
    """

    first = await get_population(city1)
    second = await get_population(city2)

    p1 = first["population"]
    p2 = second["population"]

    if p1 >= p2:
        larger = city1
        difference = p1 - p2
    else:
        larger = city2
        difference = p2 - p1

    return {
        "success": True,
        "city1": first,
        "city2": second,
        "larger_city": larger,
        "population_difference": difference,
    }


async def health_check() -> dict[str, Any]:
    """
    Population MCP health check.
    """

    return {
        "service": "Population MCP",
        "status": "healthy",
    }