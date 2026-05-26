# Task 2 – Pipeline Building

A Python-based ETL pipeline that fetches data from a 
public API, transforms it, and loads it into BigQuery.

## What This Task Is About
Building a small but complete data pipeline that demonstrates:
- API integration
- Data transformation
- BigQuery loading
- Production thinking

## Pipeline Steps
- [x] Step 1: Choose public API — Open-Meteo ✅
- [x] Step 2: BigQuery project and dataset created ✅
- [ ] Step 3: Fetch data with error handling
- [ ] Step 4: Transform and clean data
- [ ] Step 5: Load into BigQuery
- [ ] Step 6: Write SQL summary query
- [ ] Step 7: Document production approach

## API Chosen
Open-Meteo — weather data, no API key required

**Why Open-Meteo:**
### Why I Chose Open-Meteo

It requires no API key setup and returns structured hourly JSON data that is useful for ETL transformations. It let me focus more on pipeline design, data cleaning, and loading instead of authentication setup.

## BigQuery Setup
- Project: weather-etl-pipeline-497515
- Dataset: weather_analytics
- Location: asia-south1 (Mumbai)

## Status
Day 2 — API selected, BigQuery configured, pipeline 
code begins Day 3.
