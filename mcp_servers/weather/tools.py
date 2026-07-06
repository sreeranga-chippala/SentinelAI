"""
SentinelAI - Weather MCP Tools

Production-ready weather tools for the Weather MCP Server.

Author: SentinelAI
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

OPENWEATHER_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"


class WeatherToolException(Exception):
    """Raised when weather retrieval fails."""


async def get_current_weather(
    city: str,
    country: str | None = None,
    units: str = "metric",
) -> dict[str, Any]:
    """
    Fetch current weather from OpenWeather.

    Args:
        city: City name.
        country: Optional country code.
        units: metric | imperial | standard

    Returns:
        Dictionary containing weather information.

    Raises:
        WeatherToolException
    """

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        raise WeatherToolException(
            "OPENWEATHER_API_KEY environment variable is not configured."
        )

    location = city

    if country:
        location = f"{city},{country}"

    params = {
        "q": location,
        "appid": api_key,
        "units": units,
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                OPENWEATHER_ENDPOINT,
                params=params,
            )

        response.raise_for_status()

        payload = response.json()

    except httpx.HTTPStatusError as exc:
        logger.exception("OpenWeather returned an HTTP error.")

        try:
            error_body = exc.response.json()
        except Exception:
            error_body = exc.response.text

        raise WeatherToolException(
            f"HTTP {exc.response.status_code}: {error_body}"
        ) from exc

    except httpx.RequestError as exc:
        logger.exception("Unable to contact OpenWeather.")
        raise WeatherToolException(
            "Unable to connect to OpenWeather."
        ) from exc

    weather = payload["weather"][0]
    main = payload["main"]
    wind = payload.get("wind", {})
    clouds = payload.get("clouds", {})
    coord = payload.get("coord", {})
    sys = payload.get("sys", {})

    return {
        "success": True,
        "city": payload.get("name"),
        "country": sys.get("country"),
        "coordinates": {
            "latitude": coord.get("lat"),
            "longitude": coord.get("lon"),
        },
        "weather": {
            "main": weather.get("main"),
            "description": weather.get("description"),
            "icon": weather.get("icon"),
        },
        "temperature": {
            "current": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "minimum": main.get("temp_min"),
            "maximum": main.get("temp_max"),
        },
        "humidity": main.get("humidity"),
        "pressure": main.get("pressure"),
        "visibility": payload.get("visibility"),
        "wind": {
            "speed": wind.get("speed"),
            "direction": wind.get("deg"),
            "gust": wind.get("gust"),
        },
        "cloudiness": clouds.get("all"),
        "timestamp": payload.get("dt"),
    }


async def health_check() -> dict[str, Any]:
    """
    Weather MCP health check.

    Returns:
        Status dictionary.
    """

    return {
        "service": "Weather MCP",
        "status": "healthy",
    }