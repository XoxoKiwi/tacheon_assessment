# Pipeline configuration and parameters

# --- API Configuration ---
API_BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Cities to fetch weather data for
# Each entry: (city_name, latitude, longitude)
CITIES = [
    ("Chennai", 13.0827, 80.2707),
    ("Mumbai", 19.0760, 72.8777),
    ("Delhi", 28.6139, 77.2090),
    ("Bengaluru", 12.9716, 77.5946),
]

# Weather variables to request from Open-Meteo
DAILY_VARIABLES = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "uv_index_max",
    "windspeed_10m_max",
    "precipitation_hours",
]

# Number of past days to fetch (Open-Meteo supports up to 92 days)
PAST_DAYS = 7

# Timezone for API requests
TIMEZONE = "Asia/Kolkata"

# --- Transformation Thresholds ---
HEATWAVE_TEMP_THRESHOLD = 35.0        # degrees Celsius
RAINY_PRECIPITATION_THRESHOLD = 2.5   # mm
CLOUDY_PRECIPITATION_THRESHOLD = 0.1  # mm

# UV risk level thresholds
UV_LOW_MAX = 2
UV_MODERATE_MAX = 5
UV_HIGH_MAX = 7
# Above 7 = Very High

# Campaign condition score weights
UV_SCORE_WEIGHT = 0.6
TEMP_SCORE_WEIGHT = 0.4
UV_INDEX_MAX_REFERENCE = 11.0         # normalization reference
TEMP_MAX_REFERENCE = 45.0             # normalization reference (degrees Celsius)

# --- BigQuery Configuration ---
GCP_PROJECT_ID = "weather-etl-pipeline-497515"
BIGQUERY_DATASET = "weather_analytics"
BIGQUERY_TABLE = "daily_weather"
BIGQUERY_LOCATION = "asia-south1"

# Full table reference
BIGQUERY_TABLE_ID = f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}"

# Write disposition: WRITE_APPEND adds new rows without overwriting existing data
BIGQUERY_WRITE_DISPOSITION = "WRITE_APPEND"
