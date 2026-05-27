# Data extraction — fetch raw weather data from Open-Meteo API

import requests
from typing import Optional
from logger import get_logger
from config import (
    API_BASE_URL,
    CITIES,
    DAILY_VARIABLES,
    PAST_DAYS,
    TIMEZONE,
)

logger = get_logger(__name__)


def fetch_weather_for_city(
    city_name: str,
    latitude: float,
    longitude: float,
) -> Optional[dict]:
    """
    Fetches raw daily weather data for a single city from Open-Meteo API.
    Returns the raw JSON response or None if the request fails.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join(DAILY_VARIABLES),
        "past_days": PAST_DAYS,
        "timezone": TIMEZONE,
        "forecast_days": 1,
    }

    logger.info(f"Fetching weather data for {city_name} (lat={latitude}, lon={longitude})")

    try:
        response = requests.get(API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Validate that expected keys exist in the response
        if "daily" not in data:
            logger.error(f"Unexpected response structure for {city_name} — 'daily' key missing")
            return None

        logger.info(f"Successfully fetched {len(data['daily']['time'])} days of data for {city_name}")
        return data

    except requests.exceptions.Timeout:
        logger.error(f"Request timed out for {city_name}")
        return None

    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error while fetching data for {city_name}")
        return None

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error for {city_name}: {e}")
        return None

    except Exception as e:
        logger.error(f"Unexpected error for {city_name}: {e}")
        return None


def fetch_all_cities() -> list[dict]:
    """
    Iterates over all configured cities and fetches weather data for each.
    Returns a list of raw API responses with city name attached.
    Skips cities where the request failed.
    """
    results = []

    for city_name, latitude, longitude in CITIES:
        raw_data = fetch_weather_for_city(city_name, latitude, longitude)

        if raw_data is not None:
            # Attach city name to raw response for use in transformation step
            raw_data["city_name"] = city_name
            results.append(raw_data)
        else:
            logger.warning(f"Skipping {city_name} — no data returned")

    logger.info(f"Extraction complete — {len(results)}/{len(CITIES)} cities fetched successfully")
    return results


if __name__ == "__main__":
    # Quick test run
    data = fetch_all_cities()
    for d in data:
        print(f"{d['city_name']}: {len(d['daily']['time'])} days fetched")