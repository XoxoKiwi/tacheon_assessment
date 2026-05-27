# Walkthrough — Task 2: Pipeline Building

A written narrative of my thinking process — what I chose, why I built it this way, and what I would do differently with more time.

---

## Where I Started

The brief asked me to build a small but complete data pipeline using any public API. The emphasis was on demonstrating I could structure a real engineering workflow — not just write a script that fetches data.

My first decision was the API. I chose Open-Meteo because it is free, requires no API key, returns structured JSON with a stable schema, and is genuinely reliable. It removed all setup friction and let me focus on the pipeline architecture itself.

---

## The Architecture Decision

I separated the pipeline into five distinct files — `extract.py`, `transform.py`, `load.py`, `config.py`, and `logger.py` — with `pipeline.py` as the orchestrator.

I could have written everything in a single script. I deliberately didn't.

The reason: the brief asked me to think about production. A single-file script is not production-ready — it's hard to debug, impossible to test in parts, and fragile when one step fails. Separating extract, transform, and load means each step can fail independently, be retried independently, and be read independently. That mirrors how real pipelines are built.

---

## The Config Decision

Every configurable value — city coordinates, API variables, BigQuery project ID, transformation thresholds — lives in `config.py`. Nothing is hardcoded in the logic files.

This was a direct response to the brief's requirement to "avoid hardcoding values like dates, endpoints, or limits directly into logic." But it's also just good engineering practice. If the team wants to add a new city or change a threshold, they change one file, not hunt through the codebase.

---

## The Transformation Thinking

Raw API responses are rarely useful as-is. The brief asked for at least one meaningful derived field — I added four.

**weather_category** — classifies each day as Sunny, Rainy, or Cloudy based on precipitation. Simple but immediately readable.

**heatwave_flag** — boolean flag for days above 35°C. Operationally useful for any brand making weather-dependent decisions.

**uv_risk_level** — WHO UV index classification. Adds interpretability to a raw number.

**campaign_condition_score** — this is the most interesting one. A 0–100 score estimating how favourable conditions are for a skincare brand's paid campaigns, weighted by UV index and temperature. It is the kind of derived signal that would actually be useful in a marketing context — it connects raw weather data to a business decision.

The score formula is simple and transparent:
```
score = (uv_index/11 × 0.6 + temperature_max/45 × 0.4) × 100
```

I chose a weighted formula rather than a simple average because UV index is more directly relevant to skincare campaign performance than temperature alone.

---

## The BigQuery Decision

The brief required BigQuery specifically. I used the free Sandbox tier — no billing account needed.

One constraint I had to work around: the Sandbox does not support DML operations like UPDATE or DELETE. This meant I couldn't implement upsert logic. Instead I used `WRITE_APPEND` — each pipeline run adds new rows. In production this would need an idempotency layer to prevent duplicates on reruns, which I've noted in the production thinking section of the README.

The schema was designed to be clean and typed correctly from the start — STRING, DATE, FLOAT, BOOL — rather than loading everything as strings and fixing it later.

---

## The Error Handling Approach

Every step has explicit error handling. API timeouts, connection errors, HTTP errors, and unexpected response structures are all caught separately with clear log messages.

The pipeline uses Python's `logging` module with a consistent format across all files — timestamp, level, module, message. This means if something fails, the log immediately tells you which step failed, why, and for which city.

The pipeline also exits with a non-zero status code on failure at any step, which is essential for any scheduler to detect and alert on.

---

## What I Would Do Differently With More Time

**Add idempotent loading.** Currently if the pipeline runs twice on the same day, it inserts duplicate rows. In production I would use a date + city composite key to deduplicate on load or use a MERGE statement once on a full GCP account.

**Parameterise the date range from the command line.** Right now `PAST_DAYS` is set in config. A proper production pipeline would accept a date range as a CLI argument so it can be run for any historical window without changing config.

**Add a data quality check between transform and load.** Before uploading to BigQuery, I would validate row counts, check for nulls in required fields, and verify derived field ranges are within expected bounds. If quality checks fail, the pipeline should stop rather than load bad data.

**Write unit tests for transformation logic.** The derived field functions are pure and deterministic — they are straightforward to unit test. I would add pytest coverage for `get_weather_category`, `get_uv_risk_level`, and `get_campaign_condition_score` at minimum.

