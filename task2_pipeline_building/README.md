# Task 2 — Pipeline Building

A complete weather data ETL pipeline using the Open-Meteo API, Python, and Google BigQuery.

---

## Why Open-Meteo?

Free, no API key required, returns structured JSON with a stable schema. Reliable enough to demonstrate a production-style ETL pipeline without setup friction.

---

## Project Structure

```
task2_pipeline_building/
├── src/
│   ├── config.py       — all parameters, no hardcoded values
│   ├── logger.py       — centralised logging setup
│   ├── extract.py      — fetch raw weather data from Open-Meteo API
│   ├── transform.py    — flatten, clean, and enrich API response
│   ├── load.py         — upload transformed data to BigQuery
│   └── pipeline.py     — orchestrates extract → transform → load
├── queries/
│   └── summary.sql     — analytical SQL queries on stored data
├── screenshots/        — BigQuery output screenshots
└── README.md
```

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Authenticate with Google Cloud
```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project weather-etl-pipeline-497515
```

### 3. Run the pipeline
```bash
cd task2_pipeline_building/src
python pipeline.py
```

The pipeline fetches 8 days of weather data for Chennai, Mumbai, Delhi, and Bengaluru, transforms it with derived fields, and loads 32 rows into BigQuery.

---

## BigQuery Setup

| Setting | Value |
|---|---|
| Project ID | `weather-etl-pipeline-497515` |
| Dataset | `weather_analytics` |
| Table | `daily_weather` |
| Location | `asia-south1` (Mumbai) |

The table is created automatically on first run. Uses `WRITE_APPEND` — each run adds new rows without overwriting existing data.

**Sandbox note:** This project uses the BigQuery free Sandbox tier. Tables expire after 60 days and DML operations are restricted — the pipeline uses append-only loading to stay within these constraints.

---

## Schema

| Field | Type | Description |
|---|---|---|
| city | STRING | City name |
| date | DATE | Observation date |
| temperature_max | FLOAT | Max daily temperature (°C) |
| temperature_min | FLOAT | Min daily temperature (°C) |
| precipitation | FLOAT | Daily rainfall (mm) |
| uv_index | FLOAT | Daily UV index |
| windspeed_max | FLOAT | Max wind speed (km/h) |
| precipitation_hours | FLOAT | Hours of precipitation |
| weather_category | STRING | Sunny / Rainy / Cloudy |
| heatwave_flag | BOOL | True if temp_max > 35°C |
| uv_risk_level | STRING | Low / Moderate / High / Very High |
| campaign_condition_score | FLOAT | 0–100 skincare campaign suitability score |

---

## Derived Fields

**weather_category** — classifies each day based on precipitation thresholds.

**heatwave_flag** — True when max temperature exceeds 35°C.

**uv_risk_level** — WHO UV index classification.

**campaign_condition_score** — 0–100 score for skincare campaign suitability:
```
score = (uv_index/11 × 0.6 + temperature_max/45 × 0.4) × 100
```

---

## SQL Query & Sample Output

Full queries in `queries/summary.sql`. Key query:

```sql
SELECT
    city,
    ROUND(AVG(uv_index), 2) AS avg_uv_index,
    ROUND(AVG(temperature_max), 2) AS avg_max_temp,
    ROUND(AVG(campaign_condition_score), 2) AS avg_campaign_score
FROM `weather-etl-pipeline-497515.weather_analytics.daily_weather`
GROUP BY city
ORDER BY avg_campaign_score DESC;
```

**Sample output:**

| city | avg_uv_index | avg_max_temp | avg_campaign_score |
|---|---|---|---|
| Delhi | 7.74 | 42.46 | 79.95 |
| Chennai | 8.19 | 38.69 | 79.05 |
| Mumbai | 7.56 | 33.75 | 71.22 |
| Bengaluru | 7.33 | 30.14 | 66.78 |

Screenshots of all query outputs are in `screenshots/`.

---

## Production Thinking

**Scheduling:** Apache Airflow with a daily DAG — each ETL step as a separate task for independent retries. Alternatively, Cloud Scheduler + Cloud Run for a simpler serverless setup.

**Failure detection:** Structured logs at every step routed to Google Cloud Logging, with alerting policies on ERROR-level logs. Pipeline exits with non-zero status on failure, which Airflow catches automatically.

**Scaling to 10x data volume:**
- Switch to batch file uploads via GCS instead of `load_table_from_json`
- Add BigQuery table partitioning by date to control query costs
- Move transformation to Dataflow or dbt for parallelised processing
- Implement idempotent loading using date + city as composite key to prevent duplicate rows

