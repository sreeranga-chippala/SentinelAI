"""
SentinelAI - Hospital MCP Tools
Uses:
1. OpenStreetMap Nominatim (Geocoding)
2. OpenStreetMap Overpass (Hospitals)
"""

from __future__ import annotations

from typing import Any

import httpx

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

import math


def haversine(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """
    Distance between two coordinates in KM.
    """

    R = 6371.0

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    return R * c

class HospitalToolException(Exception):
    """Hospital MCP Exception."""


async def geocode_location(
    location: str,
) -> tuple[float, float]:
    """
    Convert location name into latitude and longitude
    using OpenStreetMap Nominatim.
    """

    async with httpx.AsyncClient(
        timeout=30.0,
        headers={
            "User-Agent": "SentinelAI/1.0"
        },
    ) as client:

        response = await client.get(
            NOMINATIM_URL,
            params={
                "q": location,
                "format": "json",
                "limit": 1,
            },
        )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise HospitalToolException(
            f"Location '{location}' not found."
        )

    return (
        float(data[0]["lat"]),
        float(data[0]["lon"]),
    )


async def find_nearby_hospitals(
    location: str,
    radius: int = 5000,
) -> dict[str, Any]:
    """
    Find nearby hospitals.
    """

    latitude, longitude = await geocode_location(location)

    query = f"""
                [out:json][timeout:25];
                (
                node["amenity"="hospital"](around:{radius},{latitude},{longitude});
                way["amenity"="hospital"](around:{radius},{latitude},{longitude});
                relation["amenity"="hospital"](around:{radius},{latitude},{longitude});
                );
                out center tags;
            """

    async with httpx.AsyncClient(
        timeout=30.0,
        headers={
            "User-Agent": "SentinelAI/1.0"
        },
    ) as client:

        response = await client.post(
            OVERPASS_URL,
            data=query,
        )

    response.raise_for_status()

    payload = response.json()

    hospitals = []

    for element in payload.get("elements", []):

        tags = element.get("tags", {})

        if "lat" in element:

            lat = element["lat"]
            lon = element["lon"]

        else:

            center = element.get("center", {})

            lat = center.get("lat")
            lon = center.get("lon")

        if lat is None or lon is None:
            continue

        distance = round(
            haversine(
                latitude,
                longitude,
                lat,
                lon,
            ),
            2,
        )

        hospitals.append(
            {
                "hospital_id": element["id"],
                "name": tags.get(
                    "name",
                    "Unnamed Hospital",
                ),
                "latitude": lat,
                "longitude": lon,
                "distance_km": distance,
                "phone": tags.get("phone"),
                "operator": tags.get("operator"),
                "emergency": tags.get(
                    "emergency",
                    "unknown",
                ),
            }
        )

    hospitals.sort(
        key=lambda hospital: hospital["distance_km"]
    )

    hospitals = hospitals[:10]

    return {
        "success": True,
        "location": location,
        "count": len(hospitals),
        "search_radius_m": radius,
        "hospitals": hospitals,
    }

    

async def health_check():

    return {
        "service": "Hospital MCP",
        "status": "healthy",
    }