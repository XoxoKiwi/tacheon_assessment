# Transformation logic — flatten and enrich API response data

from typing import Optional
from logger import get_logger
from config import (
    HEATWAVE_TEMP_THRESHOLD,
    RAINY_PRECIPITATION_THRESHOLD,
    CLOUDY_PRECIPITATION_THRESHOLD,
    UV_LOW_MAX,
    UV_MODERATE_MAX,
    UV_HIGH_MAX,
    UV_SCORE_WEIGHT,
    TEMP_SCORE_WEIGHT,
    UV_INDEX_MAX_REFERENCE,
    TEMP_MAX_REFERENCE,
)

logger = get_logger(__name__)


def get_weather_category(precipitation: Optional[float]) -> str:
    """
    Classifies weather as Sunny, Rainy, or Cloudy based on precipitation.
    """
    if precipitation is None:
        return "Unknown"
    if precipitation >= RAINY_PRECIPITATION_THRESHOLD:
        return "Rainy"
    if precipitation >= CLOUDY_PRECIPITATION_THRESHOLD:
        return "Cloudy"
    return "Sunny"


def get_uv_risk_level(uv_index: Optional[float]) -> str:
    """
    Returns UV risk category based on WHO UV index classifications.
    """
    if uv_index is None:
        return "Unknown"
    if uv_index <= UV_LOW_MAX:
        return "Low"
    if uv_index <= UV_MODERATE_MAX:
        return "Moderate"
    if uv_index <= UV_HIGH_MAX:
        return "High"
    return "Very High"


def get_heatwave_flag(temperature_max: Optional[float]) -> bool:
    """
    Returns True if max temperature exceeds heatwave threshold.
    """
    if temperature_max is None:
        return False
    return temperature_max > HEATWAVE_TEMP_THRESHOLD


def get_campaign_condition_score(
    uv_index: Optional[float],
    temperature_max: Optional[float],
) -> Optional[float]:
    """
    Calculates a 0-100 score estimating how favourable weather conditions
    are for skincare-related marketing campaigns.

    Higher UV index and higher temperature = higher score.
    Formula: (UV_normalized * 0.6) + (Temp_normalized * 0.4) * 100
    """
    if uv_index is None or temperature_max is None:
        return None

    uv_normalized = min(uv_index / UV_INDEX_MAX_REFERENCE, 1.0)
    temp_normalized = min(temperature_max / TEMP_MAX_REFERENCE, 1.0)

    score = (uv_normalized * UV_SCORE_WEIGHT + temp_normalized * TEMP_SCORE_WEIGHT) * 100
    return round(score, 2)


def safe_float(value) -> Optional[float]:
    """
    Safely converts a value to float. Returns None if conversion fails.
    """
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def transform_city_data(raw_data: dict) -> list[dict]:
    """
    Flattens and enriches raw Open-Meteo API response for a single city.
    Returns a list of row dicts — one row per day.
    """
    city_name = raw_data.get("city_name", "Unknown")
    daily = raw_data.get("daily", {})

    dates = daily.get("time", [])
    temp_max_list = daily.get("temperature_2m_max", [])
    temp_min_list = daily.get("temperature_2m_min", [])
    precipitation_list = daily.get("precipitation_sum", [])
    uv_index_list = daily.get("uv_index_max", [])
    windspeed_list = daily.get("windspeed_10m_max", [])
    humidity_list = daily.get("relativehumidity_2m_max", [])

    rows = []

    for i, date in enumerate(dates):
        try:
            temp_max = safe_float(temp_max_list[i] if i < len(temp_max_list) else None)
            temp_min = safe_float(temp_min_list[i] if i < len(temp_min_list) else None)
            precipitation = safe_float(precipitation_list[i] if i < len(precipitation_list) else None)
            uv_index = safe_float(uv_index_list[i] if i < len(uv_index_list) else None)
            windspeed = safe_float(windspeed_list[i] if i < len(windspeed_list) else None)
            humidity = safe_float(humidity_list[i] if i < len(humidity_list) else None)

            row = {
                "city": city_name,
                "date": date,
                "temperature_max": temp_max,
                "temperature_min": temp_min,
                "precipitation": precipitation,
                "uv_index": uv_index,
                "windspeed_max": windspeed,
                "humidity": humidity,
                # Derived fields
                "weather_category": get_weather_category(precipitation),
                "heatwave_flag": get_heatwave_flag(temp_max),
                "uv_risk_level": get_uv_risk_level(uv_index),
                "campaign_condition_score": get_campaign_condition_score(uv_index, temp_max),
            }

            rows.append(row)

        except Exception as e:
            logger.warning(f"Skipping row {i} for {city_name} on {date} — error: {e}")
            continue

    logger.info(f"Transformed {len(rows)} rows for {city_name}")
    return rows


def transform_all(raw_data_list: list[dict]) -> list[dict]:
    """
    Transforms raw API responses for all cities into a flat list of rows
    ready for BigQuery loading.
    """
    all_rows = []

    for raw_data in raw_data_list:
        city_name = raw_data.get("city_name", "Unknown")
        rows = transform_city_data(raw_data)

        if not rows:
            logger.warning(f"No rows produced for {city_name} after transformation")
            continue

        all_rows.extend(rows)

    logger.info(f"Transformation complete — {len(all_rows)} total rows ready for loading")
    return all_rows