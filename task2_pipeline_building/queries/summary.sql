-- Summary SQL Queries — Weather Analytics
-- Project: weather-etl-pipeline-497515
-- Dataset: weather_analytics
-- Table: daily_weather

-- ============================================================
-- Query 1: Average UV Index and Max Temperature by City
-- Shows which cities have the highest UV exposure and heat
-- ============================================================
SELECT
    city,
    ROUND(AVG(uv_index), 2) AS avg_uv_index,
    ROUND(AVG(temperature_max), 2) AS avg_max_temp,
    ROUND(AVG(campaign_condition_score), 2) AS avg_campaign_score
FROM
    `weather-etl-pipeline-497515.weather_analytics.daily_weather`
GROUP BY
    city
ORDER BY
    avg_campaign_score DESC;


-- ============================================================
-- Query 2: Number of Heatwave Days per City
-- Identifies cities with extreme heat conditions
-- ============================================================
SELECT
    city,
    COUNTIF(heatwave_flag = TRUE) AS heatwave_days,
    COUNT(*) AS total_days
FROM
    `weather-etl-pipeline-497515.weather_analytics.daily_weather`
GROUP BY
    city
ORDER BY
    heatwave_days DESC;


-- ============================================================
-- Query 3: Weather Category Distribution
-- Breakdown of Sunny / Rainy / Cloudy days across all cities
-- ============================================================
SELECT
    city,
    weather_category,
    COUNT(*) AS day_count
FROM
    `weather-etl-pipeline-497515.weather_analytics.daily_weather`
GROUP BY
    city,
    weather_category
ORDER BY
    city,
    day_count DESC;


-- ============================================================
-- Query 4: UV Risk Level Summary
-- Shows distribution of UV risk levels across cities
-- ============================================================
SELECT
    city,
    uv_risk_level,
    COUNT(*) AS day_count,
    ROUND(AVG(uv_index), 2) AS avg_uv_index
FROM
    `weather-etl-pipeline-497515.weather_analytics.daily_weather`
GROUP BY
    city,
    uv_risk_level
ORDER BY
    city,
    avg_uv_index DESC;


-- ============================================================
-- Query 5: Top Campaign Condition Days
-- Best days across all cities for skincare campaign targeting
-- ============================================================
SELECT
    city,
    date,
    uv_index,
    temperature_max,
    weather_category,
    campaign_condition_score
FROM
    `weather-etl-pipeline-497515.weather_analytics.daily_weather`
WHERE
    campaign_condition_score IS NOT NULL
ORDER BY
    campaign_condition_score DESC
LIMIT 10;