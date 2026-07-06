"""
SentinelAI - Traffic MCP Tools

Production-ready OpenRouteService routing tools.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

GEOCODE_ENDPOINT = (
    "https://api.openrouteservice.org/geocode/search"
)

DIRECTIONS_ENDPOINT = (
    "https://api.openrouteservice.org/v2/directions/driving-car"
)


class TrafficToolException(Exception):
    """Raised when traffic route retrieval fails."""


async def _geocode(
    client: httpx.AsyncClient,
    api_key: str,
    place: str,
) -> tuple[float, float]:
    """
    Convert a place name into longitude and latitude.
    """

    response = await client.get(
        GEOCODE_ENDPOINT,
        params={
            "api_key": api_key,
            "text": place,
            "size": 1,
        },
    )

    response.raise_for_status()

    payload = response.json()

    features = payload.get("features", [])

    if not features:
        raise TrafficToolException(
            f"Unable to locate '{place}'."
        )

    coordinates = features[0]["geometry"]["coordinates"]

    return coordinates[0], coordinates[1]


async def get_route_information(
    origin: str,
    destination: str,
) -> dict[str, Any]:
    """
    Compute a driving route.

    Args:
        origin:
            Origin city/address.

        destination:
            Destination city/address.
    """

    api_key = os.getenv(
        "OPENROUTESERVICE_API_KEY"
    )

    if not api_key:
        raise TrafficToolException(
            "OPENROUTESERVICE_API_KEY is not configured."
        )

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(
        timeout=30.0,
    ) as client:

        origin_lon, origin_lat = await _geocode(
            client,
            api_key,
            origin,
        )

        destination_lon, destination_lat = await _geocode(
            client,
            api_key,
            destination,
        )

        body = {
            "coordinates": [
                [
                    origin_lon,
                    origin_lat,
                ],
                [
                    destination_lon,
                    destination_lat,
                ],
            ]
        }

        logger.info(
            "Routing from %s to %s",
            origin,
            destination,
        )

        response = await client.post(
            DIRECTIONS_ENDPOINT,
            headers=headers,
            json=body,
        )

        response.raise_for_status()

        payload = response.json()

    routes = payload.get("routes", [])

    if not routes:
        raise TrafficToolException(
            "No route returned."
        )

    route = routes[0]

    summary = route["summary"]

    return {
    "success": True,
    "origin": origin,
    "destination": destination,
    "distance_meters": round(summary["distance"], 2),
    "distance_km": round(summary["distance"] / 1000, 2),
    "duration_seconds": round(summary["duration"], 2),
    "duration_minutes": round(summary["duration"] / 60, 2),
    "traffic_status": "NORMAL",
    "geometry": route.get("geometry"),
}


async def health_check() -> dict[str, Any]:
    """
    Traffic MCP health check.
    """

    return {
        "service": "Traffic MCP",
        "status": "healthy",
    }